from rest_framework import serializers
from . import serializers as art_serializer
from images.serializers import UploadedImagesField

class ArtPieceCreateRequestSerializer(serializers.Serializer):
    title           = serializers.CharField()
    slug            = serializers.SlugField()
    artist          = serializers.CharField(required=False, help_text="Painting, Sculpture")
    architect       = serializers.CharField(required=False, help_text="Architecture")
    photographer    = serializers.CharField(required=False, help_text="Photography")
    uploaded_images = UploadedImagesField()

ArtPieceSwaggerSerializer = art_serializer.PolymorphicProxySerializer(
    component_name="ArtPiece",
    serializers=[
        art_serializer.PaintingSerializer,
        art_serializer.ArchitectureSerializer,
        art_serializer.SculptureSerializer,
        art_serializer.PhotographySerializer,
        art_serializer.OtherSerializer
    ],
    resource_type_field_name="category"
)