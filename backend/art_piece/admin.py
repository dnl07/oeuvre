from django.contrib import admin
from .models import Painting, Architecture, Sculpture, Photography, Other
from images.models import Image
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count


class ImageInlineAdmin(GenericTabularInline):
    model = Image
    extra = 1
    fields = ["image"]
    readonly_fields = ["created_at"]

class ArtPieceBaseAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "image_count"]
    inlines = [ImageInlineAdmin]
    readonly_fields = ["slug", "created_at"]
    ordering = ("-created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_image_count=Count("images"))

    @admin.action(description="Images")
    def image_count(self, obj):
        return obj._image_count

@admin.register(Painting)
class PaintingAdmin(ArtPieceBaseAdmin):
    list_display = ArtPieceBaseAdmin.list_display + ["artist"]

@admin.register(Architecture)
class ArchitectureAdmin(ArtPieceBaseAdmin):
    pass

@admin.register(Sculpture)
class SculptureAdmin(ArtPieceBaseAdmin):
    pass

@admin.register(Photography)
class PhotographyAdmin(ArtPieceBaseAdmin):
    pass

@admin.register(Other)
class OtherAdmin(ArtPieceBaseAdmin):
    pass