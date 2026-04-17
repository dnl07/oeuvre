from images.models import Image
from .indexing.mapper import map_art_piece
from commons.search.service import SearchEngineService
from django.db import transaction

class ArtPieceService:
    @staticmethod
    def create(model, validated_data, uploaded_images=None):
        instance = model.objects.create(**validated_data)

        if uploaded_images:
            for img in uploaded_images:
                Image.objects.create(content_object=instance, image=img)

        transaction.on_commit(
            lambda: SearchEngineService().index_item(map_art_piece(instance))
        )

        return instance
    
    @staticmethod
    def update(instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        transaction.on_commit(
            lambda: SearchEngineService().update_item(map_art_piece(instance))
        )

        return instance        
    
    @staticmethod
    def delete(instance):
        instance.delete()

        transaction.on_commit(
            lambda: SearchEngineService().delete_item(instance.search_id)
        )