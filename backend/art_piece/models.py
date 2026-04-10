from django.db import models

class ArtPieceBase(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Artwork(ArtPieceBase):
    artist = models.CharField(max_length=100)

class Architecture(ArtPieceBase):
    architect = models.CharField(max_length=100)

class Sculpture(ArtPieceBase):
    artist = models.CharField(max_length=100)

class Photography(ArtPieceBase):
    photographer = models.CharField(max_length=100)

class Other(ArtPieceBase):
    pass