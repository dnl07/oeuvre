from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from . import models
from .serializers import ArtPiecePolymorphicSerializer
from itertools import chain
from images.serializers import UploadedImagesField
from . import swagger_serializers

class ArtPieceViewSet(ViewSet):
    serializer_class = ArtPiecePolymorphicSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

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

        images = instance.images.all()

        for image in images:
            image.delete()

        instance.delete()
        return Response(status=200)
    
    @extend_schema(request=swagger_serializers.ArtPieceSwaggerSerializer)
    def partial_update_by_id(self, request, category=None, id=None):
        model, error = self.get_model_or_400(category)
        if error:
            return error
        
        data = request.data.copy()
        data["category"] = category

        instance = get_object_or_404(model, pk=id)
        serializer = ArtPiecePolymorphicSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)        
    
    @extend_schema(
        request={
            "multipart/form-data": swagger_serializers.ArtPieceCreateRequestSerializer},
        responses=swagger_serializers.ArtPieceSwaggerSerializer,
    )
    def create_by_category(self, request, category=None):
        data = request.data.copy()
        data["category"] = category

        serializer = ArtPiecePolymorphicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)        