from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes

def art_piece_list_schema():
    return extend_schema(
        parameters=[
            OpenApiParameter(
                name="categories",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by categories"
            ),
            OpenApiParameter(
                name="year",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by year"
            ),
            OpenApiParameter(
                name="locations",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by locations"
            ),
            OpenApiParameter(
                name="artists",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by artists"
            ),
            OpenApiParameter(
                name="techniques",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by techniques"
            ),
            OpenApiParameter(
                name="measurements",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by measurements"
            ),
            OpenApiParameter(
                name="architects",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by architects"
            ),
            OpenApiParameter(
                name="materials",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by materials"
            ),
            OpenApiParameter(
                name="photographers",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by photographers"
            ),
            OpenApiParameter(
                name="cameras",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
                description="Filter by cameras"
            ),
        ]
    )