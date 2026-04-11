from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from . import models
from .serializers import ArtPiecePolymorphicSerializer, ArtPieceSwaggerSerializer
from itertools import chain

class ArtPieceViewSet(ViewSet):
    serializer_class = ArtPiecePolymorphicSerializer

    def get_model_or_400(self, category: str):
        model = models.MODEL_MAP.get(category)
        if not model:
            return None, Response({"error": f"Unknown category: {category}"}, status=400)
        return model, None

    def list(self, request):
        queryset = list(chain(*[m.objects.all() for m in models.MODEL_MAP.values()]))
        serializer = ArtPiecePolymorphicSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve_by_id(self, request, category=None, id=None):
        model, error = self.get_model_or_400(category)
        if error:
            return error
        instance = get_object_or_404(model, pk=id)
        serializer = ArtPiecePolymorphicSerializer(instance)
        return Response(serializer.data)

    def delete_by_id(self, request, category=None, id=None):
        model, error = self.get_model_or_400(category)
        if error:
            return error
        instance = get_object_or_404(model, pk=id)
        instance.delete()
        return Response(status=200)
    
    @extend_schema(request=ArtPieceSwaggerSerializer)
    def create_by_category(self, request, category=None):
        data = request.data.copy()
        data["category"] = category

        serializer = ArtPiecePolymorphicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)        