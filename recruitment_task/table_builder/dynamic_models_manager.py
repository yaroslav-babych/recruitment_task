from django.apps import apps
from django.db import models, connection
from django.db.models import Model
from django.db.models.base import ModelBase

from recruitment_task.table_builder.constants import FIELD_TYPES_MAP
from recruitment_task.table_builder.validators import validate_fields, validate_if_type_change_attempt


class DynamicModelMeta(ModelBase):
    def __new__(cls, model_name: str, fields: dict, app_label: str) -> type[Model]:
        model_fields = {
            "__module__": "",
            "Meta": type("Meta", (), {"app_label": app_label})
        }

        for field_name, field_type in fields.items():
            model_fields[field_name] = FIELD_TYPES_MAP[field_type]

        # Call the parent's __new__ method to create the new model class
        return super().__new__(cls, model_name, (models.Model,), model_fields)


def get_model(app_name: str, model_name: str):
    return apps.get_model(app_name, model_name)


def create_model(app_name: str, model_name: str, fields: dict) -> DynamicModelMeta:
    validate_fields(fields)
    # Create the dynamic model
    DynamicModel = DynamicModelMeta(model_name, fields, app_name)

    # Create corresponding table in db
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(DynamicModel)

    # Register the model with the app
    apps.register_model(app_name, DynamicModel)
    return DynamicModel


def update_model(app_name: str, model_name: str, old_fields: dict, new_fields: dict) -> DynamicModelMeta:
    """
    Raise LookupError if no application exists with this label, or no
    model exists with this name in the application. Raise ValueError if
    called with a single argument that doesn't contain exactly one dot.
    """
    validate_fields(new_fields)
    model = get_model(app_name, model_name)

    if old_fields == new_fields:
        return model

    validate_if_type_change_attempt(new_fields, old_fields)

    old_field_set = set(old_fields.keys())
    new_field_set = set(new_fields.keys())

    added_fields = new_field_set.difference(old_field_set)
    removed_fields = old_field_set.difference(new_field_set)

    added_fields_dict = {field_name: new_fields[field_name] for field_name in added_fields}
    removed_fields_dict = {field_name: old_fields[field_name] for field_name in removed_fields}

    with connection.schema_editor() as schema_editor:
        add_fields_to_model(model, added_fields_dict, schema_editor)
        remove_fields_from_model(model, removed_fields_dict, schema_editor)

    unregister_model(app_name, model_name)
    # Create a new model with the updated fields
    UpdatedModel = DynamicModelMeta(model_name, new_fields, app_name)
    # Register the updated model with the app
    apps.register_model(app_name, UpdatedModel)

    return model


def unregister_model(app_name: str, model_name: str):
    app_config = apps.get_app_config(app_name)
    model = get_model(app_name, model_name)
    del app_config.models[model_name.lower()]


def register_all_dynamic_models(app_name: str, RegistryClass: type[Model]):
    for table in RegistryClass.objects.all():
        model_name = table.model_name
        try:
            get_model(app_name, model_name)
        except LookupError:
            DynamicModel = DynamicModelMeta(model_name, table.fields, app_name)
            # Register the model with the app
            apps.register_model(app_name, DynamicModel)


def add_fields_to_model(model, fields, schema_editor):
    for field_name, field_type in fields.items():
        field = FIELD_TYPES_MAP[field_type]
        field.set_attributes_from_name(field_name)
        schema_editor.add_field(model, field)


def remove_fields_from_model(model, fields, schema_editor):
    for field_name, field_type in fields.items():
        field = model._meta.get_field(field_name)
        schema_editor.remove_field(model, field)
