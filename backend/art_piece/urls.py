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
    "patch": "partial_update_by_id",
    "delete": "delete_by_id",
})

image_view = ArtPieceViewSet.as_view({
    "post": "add_images"
})

image_detail_view = ArtPieceViewSet.as_view({
    "delete": "delete_image"
})

urlpatterns = [
    path("art-pieces/", list_view),
    path("art-pieces/<str:category>/", category_view),
    path("art-pieces/<str:category>/<int:id>", detail_view),
    path("art-pieces/<str:category>/<int:id>/images", image_view),
    path("art-pieces/<str:category>/<int:id>/images/<int:image_id>", image_detail_view)
]