from images.models import Image
from .indexing.mapper import map_art_piece
from commons.search.service import SearchEngineService
from django.db import transaction
from .models import ArtPieceBase, MODEL_MAP

class ArtPieceService:
    @staticmethod
    @transaction.atomic
    def art_piece_create(*, category, data, uploaded_images=None):
        model = MODEL_MAP.get(category)

        obj = model.objects.create(**data)

        if uploaded_images:
            for img in uploaded_images:
                Image.objects.create(content_object=obj, image=img)

        transaction.on_commit(
            lambda: SearchEngineService().index_item(map_art_piece(obj))
        )

        return obj

    @staticmethod
    @transaction.atomic
    def art_piece_update(*, obj: ArtPieceBase, data: dict):
        for attr, value in data.items():
            setattr(obj, attr, value)
        obj.save()

        transaction.on_commit(
            lambda: SearchEngineService().update_item(map_art_piece(obj))
        )

        return obj 
       
    @staticmethod
    @transaction.atomic
    def art_piece_delete(*, obj: ArtPieceBase):
        obj.delete()

        transaction.on_commit(
            lambda: SearchEngineService().delete_item(obj.search_id)
        )
    
    @staticmethod
    def art_piece_add_images(obj: ArtPieceBase, images):
        for image in images:
            Image.objects.create(content_object=obj, image=image)

        return obj
    
    def art_piece_delete_image(obj: ArtPieceBase, image_id):
        image = obj.images.filter(pk=image_id)
        image.delete()

        return obj    