from .filters import ArtPiecePolymorphicFilter
from ..domain.models import MODEL_MAP

class ArtPieceSelector:
    @staticmethod
    def art_piece_list(filters=None):
        queryset, meta = ArtPiecePolymorphicFilter(filters).apply()
        return queryset, meta

    @staticmethod
    def art_piece_get(category: str, id: int):
        model = MODEL_MAP.get(category)
        if not model:
            raise ValueError(f"Unknown category: {category}")
        return model.objects.get(pk=id)