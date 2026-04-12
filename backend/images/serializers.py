from rest_framework import serializers
from .models import Image
from drf_spectacular.utils import extend_schema_field

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image", "created_at"]
        
@extend_schema_field({
    "type": "array",
    "items": {"type": "string", "format": "binary"}
})
class UploadedImagesField(serializers.ListField):
    child = serializers.ImageField()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", True)
        super().__init__(*args, **kwargs)