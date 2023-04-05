from django.apps import AppConfig

from recruitment_task.table_builder.constants import APP_LABEL


class TableBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recruitment_task.table_builder'
    label = APP_LABEL

    def ready(self):
        """
        Register all dynamic models after app init
        """
        if self.table_exists():
            from .dynamic_models_manager import register_all_dynamic_models
            from .models import DynamicModelRegistry
            register_all_dynamic_models(APP_LABEL, DynamicModelRegistry)

    def table_exists(self):
        """
        That is needed because ready method is causing an issue because it's
        trying to query the DynamicModelRegistry table before the table is created.

        """
        from django.db import connection
        from .models import DynamicModelRegistry

        table_name = DynamicModelRegistry._meta.db_table
        tables = connection.introspection.table_names()
        return table_name in tables
