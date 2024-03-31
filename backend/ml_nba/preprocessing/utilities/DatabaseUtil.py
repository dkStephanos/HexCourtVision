import pandas as pd
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from ml_nba.models import (
    Game,
    Event,
    Moment,
    Candidate,
    CandidateFeatureVector,
    CandidateHexmap,
)


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
    def bulk_update_or_create(model_class, model_data, unique_field):
        """
        Manually implement bulk update or create functionality for any Django model class.

        Parameters:
        - model_class: The Django model class to which the operation will be applied.
        - model_data (list of dicts): A list where each dict represents data for the model instance.
        - unique_field (str): The field name used to identify unique records.
        """
        with transaction.atomic():
            # Fetch existing records' unique field values
            existing_objects = model_class.objects.filter(
                **{"%s__in" % unique_field: [item[unique_field] for item in model_data]}
            ).values_list(unique_field, flat=True)

            to_create, to_update = [], {}
            for data in model_data:
                if str(data[unique_field]) in existing_objects:
                    # Prepare a dict for updates
                    to_update[str(data[unique_field])] = data
                else:
                    # Prepare instances for creation
                    to_create.append(model_class(**data))

            # Bulk create new objects
            model_class.objects.bulk_create(to_create)

            # Fetch and update existing objects if necessary
            if to_update:
                existing_instances = model_class.objects.filter(
                    **{"%s__in" % unique_field: list(to_update.keys())}
                )
                update_fields = []
                for instance in existing_instances:
                    update_data = to_update[getattr(instance, unique_field)]
                    for field in update_data.keys():
                        if field != unique_field:
                            update_fields.append(field)
                            setattr(instance, field, update_data[field])
                # Perform the bulk update
                model_class.objects.bulk_update(existing_instances, update_fields)

    @staticmethod
    def clear_game_related_data(game_id):
        """
        Clears all data related to a specific game, including Events, Moments, Candidates,
        and their related data, before deleting the Game record itself.
        """
        if not DatabaseUtil.check_game_exists(game_id):
            raise Exception(
                f"Cannot clear game related data for id: {game_id} -- No game data found!"
            )

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

    @staticmethod
    def get_moments_for_event(event_id):
        # Fetch data from the database
        moments_list = list(Moment.objects.filter(event_id=event_id).values())

        # Create a DataFrame from the list
        moments = pd.DataFrame(moments_list)

        # Convert 'player_id' and 'team_id' to integers
        # Ensure first that these columns do not contain any NaN or None values
        # If they do, you need to handle them before conversion
        moments['player_id'] = moments['player_id'].fillna(-1).astype(int)
        moments['team_id'] = moments['team_id'].fillna(-1).astype(int)
        
        return moments