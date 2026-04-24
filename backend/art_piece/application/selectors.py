from .filters import ArtPiecePolymorphicFilter
from ..domain.models import MODEL_MAP
from commons.search.service import SearchEngineService

class ArtPieceSelector:
    @staticmethod
    def _search(query_params) -> list[int]:
        """Perform a search and return a list of search ids."""
        search_ids = []

        query = query_params.get("query")

        if not query or query.strip() == "":
            return search_ids

        engine = SearchEngineService()

        hits = engine.search(query)["hits"]
        search_ids = [hit["id"] for hit in hits]

        return search_ids

    @staticmethod
    def art_piece_list(filters=None):
        search_ids = ArtPieceSelector._search(filters)

        queryset, meta = ArtPiecePolymorphicFilter(filters).apply(search_ids)
        return queryset, meta

    @staticmethod
    def art_piece_get(category: str, id: int):
        model = MODEL_MAP.get(category)
        if not model:
            raise ValueError(f"Unknown category: {category}")
        return model.objects.get(pk=id)