from commons.search.service import IndexItem
from art_piece import models

def _map_painting(obj: models.Painting) -> IndexItem:
    fields_for_description = ["location", "artist", "technique"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.search_id,
        title=obj.title,
        description=description,
        tags=["painting"]
    )

def _map_architecture(obj: models.Architecture) -> IndexItem:
    fields_for_description = ["location", "architect"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.search_id,
        title=obj.title,
        description=description,
        tags=["architecture"]
    )

def _map_sculpture(obj: models.Sculpture) -> IndexItem:
    fields_for_description = ["location", "artist", "material"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.search_id,
        title=obj.title,
        description=description,
        tags=["sculpture"]
    )

def _map_photography(obj: models.Photography) -> IndexItem:
    fields_for_description = ["location", "photographer", "camera"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.search_id,
        title=obj.title,
        description=description,
        tags=["photography"]
    )

def _map_other(obj: models.Other) -> IndexItem:
    fields_for_description = ["location"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.search_id,
        title=obj.title,
        description=description,
        tags=["other"]
    )

MAPPER_MAP = {
    models.Painting: _map_painting,
    models.Architecture: _map_architecture,
    models.Sculpture: _map_sculpture,
    models.Photography: _map_photography,
    models.Other: _map_other,
}

def map_art_piece(obj):
    model = type(obj)
    mapper = MAPPER_MAP.get(model)
    return mapper(obj)