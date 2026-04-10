from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"art-pieces", views.ArtPieceViewSet, basename="art-piece")

urlpatterns = [
    *router.urls
]