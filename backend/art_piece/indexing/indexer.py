from commons.search.service import SearchEngineService
from .mapper import MAPPER_MAP

def index_all_art_pieces():
    engine = SearchEngineService()

    items = []
    for (model, mapper) in MAPPER_MAP.items():
        for obj in model.objects.all():
            items.append(mapper(obj))

    engine.index_items_bulk(items)