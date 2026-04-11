from django.urls import path
from .views import ArtPieceViewSet

list_view = ArtPieceViewSet.as_view({
    "get": "list"
})

category_view = ArtPieceViewSet.as_view({
    "post": "create_by_category"
})

detail_view = ArtPieceViewSet.as_view({
    "get": "retrieve_by_id",
    "delete": "delete_by_id"
})

urlpatterns = [
    path("art-pieces/", list_view),
    path("art-pieces/<str:category>/", category_view),
    path("art-pieces/<str:category>/<int:id>", detail_view)
]