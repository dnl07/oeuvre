from django.contrib import admin
from .models import Painting, Architecture, Sculpture, Photography, Other

@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "artist", "category"]

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
