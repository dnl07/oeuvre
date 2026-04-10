from rest_framework.viewsets import ViewSet
from rest_framework.response import Response 
from . import models
from . import serializers


class ArtPieceViewSet(ViewSet):
    def list(self, request):
        queryset = models.Artwork.objects.all()
        serializer = serializers.ArtworkSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
