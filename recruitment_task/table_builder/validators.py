from rest_framework.exceptions import ValidationError
import re

from recruitment_task.table_builder.constants import FIELD_TYPES_MAP, postgres_constraints


def validate_field_type(field_type: str) -> None:
    if field_type not in FIELD_TYPES_MAP:
        raise ValidationError(f"Invalid field type '{field_type}'.")


def validate_field_name(field_name: str) -> None:
    if len(field_name) >= postgres_constraints.COLUMN_NAME_MAX_LENGTH:
        raise ValidationError(
            f"Invalid field name '{field_name}'. Must be a string shorter than {postgres_constraints.COLUMN_NAME_MAX_LENGTH} characters.")
    if not re.match(r"^[a-z_][a-zA-Z0-9_]*$", field_name):
        raise ValidationError(
            f"Invalid field name '{field_name}'. Must start with a lowercase letter or an underscore, and contain only alphanumeric characters and underscores.")


def validate_fields(fields: dict):
    if not fields:
        raise ValidationError("At least one field is required.")

    for field_name, field_type in fields.items():
        validate_field_name(field_name)
        validate_field_type(field_type)


def validate_if_type_change_attempt(new_fields: dict, old_fields: dict):
    for field_name, field_type in old_fields.items():
        if field_name in new_fields and new_fields[field_name] != field_type:
            raise ValidationError(
                f"Changing field type is not supported: {field_name} (from {field_type} to {new_fields[field_name]})")


def validate_python_class_name(value):
    if not re.match(r"^[A-Z][a-zA-Z0-9]*$", value):
        raise ValidationError(
            f"{value} is not a valid Python class name. It must start with an uppercase letter and contain only alphanumeric characters."
        )
