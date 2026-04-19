from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes
from .serializers import ArtPieceSwaggerOutputSerializer, ArtPieceCreateRequestSerializer

CATEGORY_PARAMETER = OpenApiParameter(
    name="category",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    enum=["painting", "architecture", "sculpture", "photography", "other"],
    description="Art piece category"
)

ID_PARAMETER = OpenApiParameter(
    name="id",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.PATH,
    description="Art piece id"
)


def art_piece_list_schema():
    return extend_schema(
        summary="List all art pieces",
        parameters=[
            OpenApiParameter(
                name="query",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search"
            ),
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
        ],
        responses=ArtPieceSwaggerOutputSerializer
    )

def art_piece_detail_schema():
    return extend_schema(
        summary="Create an art piece",
        parameters=[CATEGORY_PARAMETER, ID_PARAMETER],
        responses=ArtPieceSwaggerOutputSerializer
    )

def art_piece_create_schema():
    return extend_schema(
        summary="Create an art piece",
        parameters=[CATEGORY_PARAMETER],
        request={"multipart/form-data": ArtPieceCreateRequestSerializer},
        responses={201: ArtPieceSwaggerOutputSerializer},
    )