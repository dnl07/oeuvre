from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from . import models
from . import serializers
from itertools import chain

class ArtPieceViewSet(ViewSet):
    def list(self, request):
        queryset = list(chain(*[m.objects.all() for m in models.MODEL_MAP.values()]))
        serializer = serializers.ArtPiecePolymorphicSerializer(queryset, many=True)
        return Response(serializer.data)
