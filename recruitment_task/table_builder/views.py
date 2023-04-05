from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from recruitment_task.table_builder.dynamic_models_manager import get_model
from recruitment_task.table_builder.models import DynamicModelRegistry, app_name
from recruitment_task.table_builder.serializers import DynamicModelRegistrySerializer, generate_model_serializer, \
    DynamicModelRegistryUpdateSerializer


class DynamicModelRegistryViewSet(viewsets.ModelViewSet):
    queryset = DynamicModelRegistry.objects.all()
    serializer_class = DynamicModelRegistrySerializer

    http_method_names = ['get', 'post', 'put', 'options', 'head']

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return DynamicModelRegistryUpdateSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def add_row(self, request, pk=None):
        table: DynamicModelRegistry = self.get_object()
        Model = get_model(app_name, table.model_name)

        # Serialize the new row using the correct serializer
        RowSerializer = generate_model_serializer(Model)
        serializer = RowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_rows(self, request, pk=None):
        table = self.get_object()
        Model = get_model(app_name, table.model_name)
        RowSerializer = generate_model_serializer(Model)
        serializer = RowSerializer(Model.objects.all(), many=True)
        return Response(serializer.data)
