from typing import NamedTuple

from django.db import models

APP_LABEL = 'table_builder'


class DbConstraints(NamedTuple):
    TABLE_NAME_MAX_LENGTH: int
    COLUMN_NAME_MAX_LENGTH: int
    CHAR_ROW_MAX_LENGTH: int


postgres_constraints = DbConstraints(
    TABLE_NAME_MAX_LENGTH=63,
    COLUMN_NAME_MAX_LENGTH=59,
    CHAR_ROW_MAX_LENGTH=255
)
FIELD_TYPES_MAP = {
    "string": models.CharField(max_length=postgres_constraints.CHAR_ROW_MAX_LENGTH),
    "boolean": models.BooleanField(),
    "number": models.DecimalField(max_digits=10, decimal_places=2)
}
