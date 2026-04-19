from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.serializers import Serializer 
from rest_framework.parsers import MultiPartParser, FormParser
from ..application.services import ArtPieceService
from .serializers import get_input_serializer, get_output_serializer
from ..application.selectors import ArtPieceSelector
from .swagger import schemas

class ArtPieceListApi(APIView):
    class OutputSerializer(Serializer):
        def to_representation(self, instance):
            serializer_class = get_output_serializer(instance.category)
            return serializer_class(instance, context=self.context).data

    @schemas.art_piece_list_schema()
    def get(self, request):
        art_pieces, meta = ArtPieceSelector.art_piece_list(request.query_params)

        data = self.OutputSerializer(art_pieces, many=True).data

        return Response({
            "results": data,
            "meta": meta
        })        
    
class ArtPieceDetailApi(APIView):
    class OutputSerializer(Serializer):
        def to_representation(self, instance):
            serializer_class = get_output_serializer(instance.category)
            return serializer_class(instance, context=self.context).data

    @schemas.art_piece_detail_schema()
    def get(self, request, category: str, id: int):
        art_piece = ArtPieceSelector.art_piece_get(category, id)
        data = self.OutputSerializer(art_piece).data
        return Response(data)    

    @schemas.art_piece_update_schema()
    def patch(self, request, category: str, id: int):
        input_serializer = get_input_serializer(category)

        if not input_serializer:
            return Response({"error": f"Unknown category: {category}"})

        serializer = input_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = ArtPieceSelector.art_piece_get(category, id)

        instance = ArtPieceService.art_piece_update(
            obj=instance,
            data=serializer.validated_data,
        )      

        return Response(self.OutputSerializer(instance).data, status=200)
    
    @schemas.art_piece_delete_schema()
    def delete(self, request, category: str, id: int):
        instance = ArtPieceSelector.art_piece_get(category, id)

        ArtPieceService.art_piece_delete(
            obj=instance
        )
        return Response(status=204)  

class ArtPieceCreateApi(APIView):
    parser_classes = [MultiPartParser, FormParser]

    class OutputSerializer(Serializer):
        def to_representation(self, instance):
            serializer_class = get_output_serializer(instance.category)
            return serializer_class(instance, context=self.context).data

    @schemas.art_piece_create_schema()
    def post(self, request, category):
        input_serializer = get_input_serializer(category)

        if not input_serializer:
            return Response({"error": f"Unknown category: {category}"})

        serializer = input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_images = serializer.validated_data.pop("uploaded_images", [])

        instance = ArtPieceService.art_piece_create(
            category=category,
            data=serializer.validated_data,
            uploaded_images=uploaded_images
        )

        return Response(self.OutputSerializer(instance).data, status=201)


"""
class ArtPieceViewSet(ViewSet):

    def add_images(self, request, category=None, id=None):
 
        model, error = self._get_model_or_400(category)

        if error:
            return error
        
        instance = get_object_or_404(model, pk=id)
        images = request.FILES.getlist("uploaded_images")

        instance = ArtPieceService.add_images(instance, images)
    
        serializer = serializers.ArtPiecePolymorphicSerializer(instance)
        return Response(serializer.data)        
    
    def delete_image(self, request, category=None, id=None, image_id=None):

        model, error = self._get_model_or_400(category)

        if error:
            return error
        
        instance = get_object_or_404(model, pk=id)
        instance = ArtPieceService.delete_image(instance, image_id)

        serializer = serializers.ArtPiecePolymorphicSerializer(instance)
        return Response(serializer.data)
"""