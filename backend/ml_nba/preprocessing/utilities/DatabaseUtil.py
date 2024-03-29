from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from ml_nba.models import Game, Event, Moment, Candidate, CandidateFeatureVector, CandidateHexmap


class DatabaseUtil:
    """
    A utility class for extending Django ORM functionality
    """
    
    @staticmethod
    def check_game_exists(game_id):
        """
        Checks if a game with the specified game ID exists in the database.

        Parameters:
        - game_id (str): The unique identifier for the game.

        Returns:
        - bool: True if the game exists, False otherwise.
        """
        try:
            Game.objects.get(game_id=game_id)
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def bulk_update_or_create(model_class, model_data, unique_field, update_fields):
        """
        Manually implement bulk update or create functionality for any Django model class.
        
        Parameters:
        - model_class: The Django model class to which the operation will be applied.
        - model_data (list of dicts): A list where each dict represents data for the model instance.
        - unique_field (str): The field name used to identify unique records.
        - update_fields (list of str): Field names that should be updated if a record already exists.
        """
        with transaction.atomic():
            # Fetch existing records' unique field values
            existing_objects = model_class.objects.filter(
                **{"%s__in" % unique_field: [item[unique_field] for item in model_data]}
            ).values_list(unique_field, flat=True)

            to_create, to_update_ids, to_update_instances = [], [], []
            for data in model_data:
                if data[unique_field] in existing_objects:
                    # For updates, collect IDs and prepare instances with the ID set for later use
                    instance = model_class(**data)
                    to_update_ids.append(data[unique_field])
                    to_update_instances.append(instance)
                else:
                    to_create.append(model_class(**data))
            
            # Bulk create new objects
            model_class.objects.bulk_create(to_create)

            # Update existing objects
            if to_update_instances:
                # Fetch existing instances to update
                existing_instances = model_class.objects.filter(**{"%s__in" % unique_field: to_update_ids})
                # Update instances with new values
                for existing_instance in existing_instances:
                    for update_instance in to_update_instances:
                        if getattr(update_instance, unique_field) == getattr(existing_instance, unique_field):
                            for field in update_fields:
                                setattr(existing_instance, field, getattr(update_instance, field))
                            break
                model_class.objects.bulk_update(existing_instances, update_fields)
                
    @staticmethod
    def clear_game_related_data(game_id):
        """
        Clears all data related to a specific game, including Events, Moments, Candidates,
        and their related data, before deleting the Game record itself.
        """  
        if not DatabaseUtil.check_game_exists(game_id):
            raise Exception(f"Cannot clear game related data for id: {game_id} -- No game data found!")
        
        with transaction.atomic():
            # Fetch related events to the game
            events = Event.objects.filter(game__game_id=game_id)

            # Fetch related candidates to events
            candidates = Candidate.objects.filter(event__in=events)
            
            # Delete Candidate related models
            CandidateFeatureVector.objects.filter(candidate__in=candidates).delete()
            CandidateHexmap.objects.filter(candidate__in=candidates).delete()
            
            # Delete Moments and Candidates
            Moment.objects.filter(event__in=events).delete()
            candidates.delete()
            
            # Now, it's safe to delete Events and then the Game
            events.delete()
            Game.objects.filter(game_id=game_id).delete()