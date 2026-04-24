from ..domain import models
from rest_framework import serializers
from images.serializers import ImageSerializer, UploadedImagesField

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
            "photographer", "camera"
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
        fields = ArtPieceBaseInputSerializer.Meta.fields

class OtherOutputSerializer(ArtPieceBaseOutputSerializer):
    class Meta(ArtPieceBaseOutputSerializer.Meta):
        model = models.Other
        fields = ArtPieceBaseOutputSerializer.Meta.fields

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