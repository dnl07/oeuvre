from . import models
from rest_framework import serializers
from drf_spectacular.utils import PolymorphicProxySerializer
from images.serializers import ImageSerializer, UploadedImagesField
from images.models import Image
from .validators import validate_year, validate_measurements
from .services import ArtPieceService

# Base serializer with common fields
class ArtPieceBaseSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = UploadedImagesField(write_only=True)
    
    class Meta:
        abstract = True

    def validate_year(self, value):
        validate_year(value, drf=True)
        return value

# Specific serializers for each category
class PaintingSerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Painting
        fields = "__all__"
        read_only_fields = ["id", "slug"]

    def validate_measurements(self, value):
        validate_measurements(value, drf=True)
        return value

class ArchitectureSerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Architecture
        fields = "__all__"
        read_only_fields = ["id", "slug"]


class SculptureSerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Sculpture
        fields = "__all__"        
        read_only_fields = ["id", "slug"]


class PhotographySerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Photography
        fields = "__all__"
        read_only_fields = ["id", "slug"]

class OtherSerializer(ArtPieceBaseSerializer):
    class Meta:
        model = models.Other
        fields = "__all__"
        read_only_fields = ["id", "slug"]

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
        
        if self.partial:
            data = {k: v for k, v in data.items() if v != ""}
        
        serializer_class = self.get_serializer(category)
        inner = serializer_class(self.instance, data=data, context=self.context, partial=self.partial)

        inner.is_valid(raise_exception=True)
        validated = inner.validated_data
        validated["category"] = category
        return validated

    def create(self, validated_data):
        category = validated_data.pop("category")
        uploaded_images = validated_data.pop("uploaded_images", [])

        if not uploaded_images or len(uploaded_images) == 0:
            raise serializers.ValidationError({"uploaded_images": "Atleast one image is required"})

        model = models.MODEL_MAP.get(category)
        
        instance = ArtPieceService.create(model, validated_data, uploaded_images)

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
    title = serializers.CharField()
    uploaded_images = UploadedImagesField()
    year = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    artist = serializers.CharField(required=False, help_text="Painting, Sculpture")
    measurements = serializers.CharField(required=False, help_text="Painting")
    technique = serializers.CharField(required=False, help_text="Painting")
    architect = serializers.CharField(required=False, help_text="Architecture")
    photographer = serializers.CharField(required=False, help_text="Photography")
    camera = serializers.CharField(required=False, help_text="Photography")
    material = serializers.CharField(required=False, help_text="Sculpture")

class ArtPiecePatchRequestSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    year = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    artist = serializers.CharField(required=False, help_text="Painting, Sculpture")
    measurements = serializers.CharField(required=False, help_text="Painting")
    technique = serializers.CharField(required=False, help_text="Painting")
    architect = serializers.CharField(required=False, help_text="Architecture")
    photographer = serializers.CharField(required=False, help_text="Photography")
    camera = serializers.CharField(required=False, help_text="Photography")
    material = serializers.CharField(required=False, help_text="Sculpture")

class ArtPieceAddImageRequestSerializer(serializers.Serializer):
    uploaded_images = UploadedImagesField()