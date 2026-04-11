from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from . import models
from . import serializers
from itertools import chain

class ArtPieceViewSet(ViewSet):
    def list(self, request):
        queryset = list(chain(*[m.objects.all() for m in models.MODEL_MAP.values()]))
        serializer = serializers.ArtPiecePolymorphicSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path=r"(?P<category>[^/.]+)/(?P<id>[0-9]+)")
    def retrieve_by_category(self, request, category=None, id=None):
        model = models.MODEL_MAP.get(category)
        if not model:
            return Response({"error": f"Unknown category: {category}"})
        
        instance = get_object_or_404(model, pk=id)
        serializer = serializers.ArtPiecePolymorphicSerializer(instance)
        return Response(serializer.data)