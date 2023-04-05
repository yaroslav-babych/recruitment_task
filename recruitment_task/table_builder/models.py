from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from recruitment_task.table_builder import dynamic_models_manager
from recruitment_task.table_builder.constants import postgres_constraints, APP_LABEL
from recruitment_task.table_builder.validators import validate_python_class_name

app_name = APP_LABEL


class DynamicModelRegistry(models.Model):
    model_name = models.CharField(
        max_length=postgres_constraints.TABLE_NAME_MAX_LENGTH,
        unique=True,
        validators=[validate_python_class_name, ]
    )
    fields = models.JSONField()

    class Meta:
        app_label = APP_LABEL


@receiver(pre_save, sender=DynamicModelRegistry)
def create_or_update_dynamic_model(sender, instance, **kwargs):
    if instance.pk is None:
        # The model is being created, not updated
        dynamic_models_manager.create_model(app_name, str(instance.model_name), instance.fields)
    else:
        # The model is being updated
        old_instance = sender.objects.get(pk=instance.pk)
        dynamic_models_manager.update_model(app_name, str(instance.model_name), old_instance.fields, instance.fields)
