from rest_framework import serializers
from drf_spectacular.utils import PolymorphicProxySerializer
from images.serializers import UploadedImagesField
from ..serializers import OUTPUT_SERIALIZER_MAP


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