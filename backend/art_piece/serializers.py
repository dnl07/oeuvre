from . import models
from rest_framework import serializers
from drf_spectacular.utils import PolymorphicProxySerializer
from images.serializers import ImageSerializer, UploadedImagesField
from images.models import Image

# Base serializer with common fields
class ArtPieceBaseSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = UploadedImagesField(write_only=True)
    
    class Meta:
        abstract = True

# Specific serializers for each category
class PaintingSerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Painting
        fields = "__all__"

class ArchitectureSerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Architecture
        fields = "__all__"

class SculptureSerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Sculpture
        fields = "__all__"

class PhotographySerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Photography
        fields = "__all__"

class OtherSerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Other
        fields = "__all__"

# Map category to model and serializer
SERIALIZER_MAP = {
    "painting": PaintingSerializer,
    "architecture": ArchitectureSerializer,
    "sculpture": SculptureSerializer,
    "photography": PhotographySerializer,
    "other": OtherSerializer,    
}

# Polymorphic serializer that delegates to the correct serializer based on the category
class ArtPiecePolymorphicSerializer(serializers.Serializer):
    def get_serializer(self, category):
        serializer_class = SERIALIZER_MAP.get(category)
        if not serializer_class:
            raise serializers.ValidationError({"category": f"Unknown category: {category}"})
        return serializer_class

    def to_representation(self, instance):
        serializer_class = self.get_serializer(instance.category)
        return serializer_class(instance, context=self.context).data
    
    def to_internal_value(self, data):
        category = data.get("category")
        if not category:
            raise serializers.ValidationError({"category": "Required field"})
        serializer_class = self.get_serializer(category)
        inner = serializer_class(self.instance, data=data, context=self.context, partial=self.partial)
        inner.is_valid(raise_exception=True)

        validated = inner.validated_data
        validated["category"] = category
        return validated

    def create(self, validated_data):
        category = validated_data.pop("category")
        uploaded_images = validated_data.pop("uploaded_images", [])

        model = models.MODEL_MAP.get(category)
        instance = model.objects.create(**validated_data)

        for img in uploaded_images:
            Image.objects.create(content_object=instance, image=img)

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
# Serializer for Swagger documentation
ArtPieceSwaggerSerializer = PolymorphicProxySerializer(
    component_name="ArtPiece",
    serializers=list(SERIALIZER_MAP.values()),
    resource_type_field_name="category"
)

class ArtPieceCreateRequestSerializer(serializers.Serializer):
    title           = serializers.CharField()
    slug            = serializers.SlugField()
    artist          = serializers.CharField(required=False, help_text="Painting, Sculpture")
    architect       = serializers.CharField(required=False, help_text="Architecture")
    photographer    = serializers.CharField(required=False, help_text="Photography")
    uploaded_images = UploadedImagesField()

class ArtPiecePatchRequestSerializer(serializers.Serializer):
    title           = serializers.CharField(required=False)
    slug            = serializers.SlugField(required=False)
    artist          = serializers.CharField(required=False, help_text="Painting, Sculpture")
    architect       = serializers.CharField(required=False, help_text="Architecture")
    photographer    = serializers.CharField(required=False, help_text="Photography")