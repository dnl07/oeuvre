from . import models
from rest_framework import serializers
from drf_spectacular.utils import PolymorphicProxySerializer

class PaintingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Painting
        fields = "__all__"

class ArchitectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Architecture
        fields = "__all__"

class SculptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sculpture
        fields = "__all__"

class PhotographySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photography
        fields = "__all__"

class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Other
        fields = "__all__"

SERIALIZER_MAP = {
    "painting": PaintingSerializer,
    "architecture": ArchitectureSerializer,
    "sculpture": SculptureSerializer,
    "photography": PhotographySerializer,
    "other": OtherSerializer,    
}

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
            raise serializers.ValidationError({"category": "Mandatory field"})
        serializer_class = self.get_serializer(category)
        inner = serializer_class(data=data, context=self.context)
        inner.is_valid(raise_exception=True)

        validated = inner.validated_data
        validated["category"] = category
        return validated

    def create(self, validated_data):
        category = validated_data.get("category")
        model = models.MODEL_MAP.get(category)
        return model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
# For swagger
ArtPieceSwaggerSerializer = PolymorphicProxySerializer(
    component_name="ArtPiece",
    serializers=[
        PaintingSerializer,
        ArchitectureSerializer,
        SculptureSerializer,
        PhotographySerializer,
        OtherSerializer
    ],
    resource_type_field_name="category"
)