from django.contrib import admin
from .models import Painting, Architecture, Sculpture, Photography, Other
from images.models import Image
from django.contrib.contenttypes.admin import GenericTabularInline


class ImageInlineAdmin(GenericTabularInline):
    model = Image
    extra = 1
    fields = ["image", "alt_text"]
    readonly_fields = ["created_at"]

@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "artist", "category"]
    readonly_fields = ["slug", "created_at"]
    inlines = [ImageInlineAdmin, ]

@admin.register(Architecture)
class ArchitectureAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "architect"]

@admin.register(Sculpture)
class SculptureAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "artist"]

@admin.register(Photography)
class PhotographyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "photographer"]

@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    list_display = ["title"]
