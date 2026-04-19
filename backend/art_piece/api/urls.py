from django.urls import path
from . import views

urlpatterns = [
    path("art_pieces/",
        views.ArtPieceListApi.as_view(),
         name="art-piece-list" ),
    path("art_pieces/<str:category>/",
        views.ArtPieceCreateApi.as_view(),
         name="art-piece-create"),
]