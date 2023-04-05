from rest_framework import serializers
from django.db import models

from recruitment_task.table_builder.models import DynamicModelRegistry


class DynamicModelRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicModelRegistry
        fields = '__all__'


class DynamicModelRegistryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicModelRegistry
        fields = ['fields']


def generate_model_serializer(model_class: type[models.Model]) -> type[serializers.ModelSerializer]:
    meta_class = type('Meta', (object,), {'model': model_class, 'fields': '__all__'})
    serializer_class = type(f'{model_class.__name__}Serializer', (serializers.ModelSerializer,), {'Meta': meta_class})
    return serializer_class
