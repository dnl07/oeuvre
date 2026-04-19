from .. import models
from rest_framework import serializers
from images.serializers import ImageSerializer, UploadedImagesField
from drf_spectacular.utils import PolymorphicProxySerializer

class ArtPieceBaseInputSerializer(serializers.ModelSerializer):
    uploaded_images = UploadedImagesField(write_only=True)

    class Meta:
        fields = ["title", "year", "location", "uploaded_images"]

class ArtPieceBaseOutputSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta(ArtPieceBaseInputSerializer.Meta):
        fields = ["id", "title", "year", "location", "slug", "category", "images"]

class PaintingInputSerializer(ArtPieceBaseInputSerializer):
    class Meta(ArtPieceBaseInputSerializer.Meta):
        model = models.Painting
        fields = ArtPieceBaseInputSerializer.Meta.fields + [
            "artist", "technique", "measurements"
        ]

class PaintingOutputSerializer(ArtPieceBaseOutputSerializer):
    class Meta(ArtPieceBaseOutputSerializer.Meta):
        model = models.Painting
        fields = ArtPieceBaseOutputSerializer.Meta.fields + [
            "artist", "technique", "measurements"
        ]

class ArchitectureInputSerializer(ArtPieceBaseInputSerializer):
    class Meta(ArtPieceBaseInputSerializer.Meta):
        model = models.Architecture
        fields = ArtPieceBaseInputSerializer.Meta.fields + [
            "architect"
        ]

class ArchitectureOutputSerializer(ArtPieceBaseOutputSerializer):
    class Meta(ArtPieceBaseOutputSerializer.Meta):
        model = models.Architecture
        fields = ArtPieceBaseOutputSerializer.Meta.fields + [
            "architect"
        ]

class SculptureInputSerializer(ArtPieceBaseInputSerializer):
    class Meta(ArtPieceBaseInputSerializer.Meta):
        model = models.Sculpture
        fields = ArtPieceBaseInputSerializer.Meta.fields + [
            "artist", "material"
        ]

class SculptureOutputSerializer(ArtPieceBaseOutputSerializer):
    class Meta(ArtPieceBaseOutputSerializer.Meta):
        model = models.Sculpture
        fields = ArtPieceBaseOutputSerializer.Meta.fields + [
            "artist", "material"
        ]

class PhotographyInputSerializer(ArtPieceBaseInputSerializer):
    class Meta(ArtPieceBaseInputSerializer.Meta):
        model = models.Photography
        fields = ArtPieceBaseInputSerializer.Meta.fields + [
            "architect"
        ]

class PhotographyOutputSerializer(ArtPieceBaseOutputSerializer):
    class Meta(ArtPieceBaseOutputSerializer.Meta):
        model = models.Photography
        fields = ArtPieceBaseOutputSerializer.Meta.fields + [
            "photographer", "camera"
        ]

class OtherInputSerializer(ArtPieceBaseInputSerializer):
    class Meta(ArtPieceBaseInputSerializer.Meta):
        model = models.Other

class OtherOutputSerializer(ArtPieceBaseOutputSerializer):
    class Meta(ArtPieceBaseOutputSerializer.Meta):
        model = models.Other

# Map category to model and serializer
INPUT_SERIALIZER_MAP = {
    "painting": PaintingInputSerializer,
    "architecture": ArchitectureInputSerializer,
    "sculpture": SculptureInputSerializer,
    "photography": PhotographyInputSerializer,
    "other": OtherInputSerializer,    
}

OUTPUT_SERIALIZER_MAP = {
    "painting": PaintingOutputSerializer,
    "architecture": ArchitectureOutputSerializer,
    "sculpture": SculptureOutputSerializer,
    "photography": PhotographyOutputSerializer,
    "other": OtherOutputSerializer,    
}

def get_input_serializer(category):
    serializer_class = INPUT_SERIALIZER_MAP.get(category)
    if not serializer_class:
        raise serializers.ValidationError({"category": f"Unknown category: {category}"})
    return serializer_class


def get_output_serializer(category):
    serializer_class = OUTPUT_SERIALIZER_MAP.get(category)
    if not serializer_class:
        raise serializers.ValidationError({"category": f"Unknown category: {category}"})
    return serializer_class


# Serializer for Swagger documentation
ArtPieceSwaggerOutputSerializer = PolymorphicProxySerializer(
    component_name="ArtPiece",
    serializers=list(OUTPUT_SERIALIZER_MAP.values()),
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

"""
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
        category = validated_data["category"]
        uploaded_images = validated_data.pop("uploaded_images", [])

        if not uploaded_images or len(uploaded_images) == 0:
            raise serializers.ValidationError({"uploaded_images": "Atleast one image is required"})

        model = models.MODEL_MAP.get(category)
        
        instance = ArtPieceService.create(model, validated_data, uploaded_images)

        return instance

    def update(self, instance, validated_data):
        instance = ArtPieceService.update(instance, validated_data)    
        return instance
    

"""