from .models import Artwork
from rest_framework import serializers

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = "__all__"