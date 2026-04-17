from .search_engine_service import SearchEngineService, IndexItem
from art_piece import models


def _map_painting(obj: models.Painting) -> IndexItem:
    fields_for_description = ["location", "artist", "technique"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.pk,
        title=obj.title,
        description=description,
        tags=["painting"],
        metadata={
            "category": obj.category,
            "pk": str(obj.pk)
        }
    )

def _map_architecture(obj: models.Architecture) -> IndexItem:
    fields_for_description = ["location", "architect"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.pk,
        title=obj.title,
        description=description,
        tags=["architecture"],
        metadata={
            "category": obj.category,
            "pk": str(obj.pk)
        }
    )

def _map_sculpture(obj: models.Sculpture) -> IndexItem:
    fields_for_description = ["location", "artist", "material"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.pk,
        title=obj.title,
        description=description,
        tags=["sculpture"],
        metadata={
            "category": obj.category,
            "pk": str(obj.pk)
        }
    )

def _map_photography(obj: models.Photography) -> IndexItem:
    fields_for_description = ["location", "photographer", "camera"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.pk,
        title=obj.title,
        description=description,
        tags=["photography"],
        metadata={
            "category": obj.category,
            "pk": str(obj.pk)
        }
    )

def _map_other(obj: models.Other) -> IndexItem:
    fields_for_description = ["location"]
    description = ", ".join([getattr(obj, f) for f in fields_for_description if getattr(obj, f)])

    return IndexItem(
        id=obj.pk,
        title=obj.title,
        description=description,
        tags=["other"],
        metadata={
            "category": obj.category,
            "pk": str(obj.pk)
        }
    )

MAPPER_MAP = {
    "painting": (models.Painting, _map_painting),
    "architecture": (models.Architecture, _map_architecture),
    "sculpture": (models.Sculpture, _map_sculpture),
    "photography": (models.Photography, _map_photography),
    "other": (models.Other, _map_other),
}

def index_all_art_pieces():
    engine = SearchEngineService()

    items = []
    for (model, mapper) in MAPPER_MAP.values():
        for obj in model.objects.all():
            items.append(mapper(obj))

    engine.index_items_bulk(items)