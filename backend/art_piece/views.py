from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from . import serializers
from . import models
from itertools import chain
from images.models import Image


class ArtPieceViewSet(ViewSet):
    """ViewSet for handling CRUD operations on art pieces across multiple categories."""
    serializer_class = serializers.ArtPiecePolymorphicSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_model_or_400(self, category: str):
        """Helper method to get the model class based on category or 
        return a 400 response if category is invalid."""

        model = models.MODEL_MAP.get(category)
        if not model:
            return None, Response({"error": f"Unknown category: {category}"}, status=400)
        return model, None

    def list(self, request):
        """List all art pieces across all categories."""

        queryset = list(chain(*[m.objects.all() for m in models.MODEL_MAP.values()]))
        serializer = serializers.ArtPiecePolymorphicSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve_by_id(self, request, category=None, id=None):
        """Retrieve a specific art piece by category and ID."""

        model, error = self.get_model_or_400(category)
        if error:
            return error
        instance = get_object_or_404(model, pk=id)
        serializer = serializers.ArtPiecePolymorphicSerializer(instance)
        return Response(serializer.data)

    def delete_by_id(self, request, category=None, id=None):
        """Delete a specific art piece by category and ID."""

        model, error = self.get_model_or_400(category)
        if error:
            return error
        instance = get_object_or_404(model, pk=id)

        images = instance.images.all()

        for image in images:
            image.delete()

        instance.delete()
        return Response(status=200)
    
    @extend_schema(request=serializers.ArtPiecePatchRequestSerializer)
    def partial_update_by_id(self, request, category=None, id=None):
        """Partially update a specific art piece by category and ID."""

        model, error = self.get_model_or_400(category)
        if error:
            return error
        
        data = request.data.copy()
        data["category"] = category

        instance = get_object_or_404(model, pk=id)
        serializer = serializers.ArtPiecePolymorphicSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)        
    
    @extend_schema(
        request={
            "multipart/form-data": serializers.ArtPieceCreateRequestSerializer},
        responses=serializers.ArtPieceSwaggerSerializer,
    )
    def create_by_category(self, request, category=None):
        """Create a new art piece in a specific category."""

        data = request.data.copy()
        data["category"] = category

        serializer = serializers.ArtPiecePolymorphicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)        
    
    @extend_schema(request={
            "multipart/form-data": serializers.ArtPieceAddImageRequestSerializer}
    )
    def add_images(self, request, category=None, id=None):
        model, error = self.get_model_or_400(category)

        if error:
            return error
        
        instance = get_object_or_404(model, pk=id)
        images = request.FILES.getlist("uploaded_images")

        for image in images:
            Image.objects.create(content_object=instance, image=image)
    
        serializer = serializers.ArtPiecePolymorphicSerializer(instance)
        return Response(serializer.data)        
    
    def delete_image(self, request, category=None, id=None, image_id=None):
        model, error = self.get_model_or_400(category)

        if error:
            return error
        
        instance = get_object_or_404(model, pk=id)
        image = instance.images.filter(pk=image_id)

        image.delete()

        serializer = serializers.ArtPiecePolymorphicSerializer(instance)
        return Response(serializer.data)