from django.db import transaction

class DatabaseUtil:
    """
    A utility class for extending Django ORM functionality
    """

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