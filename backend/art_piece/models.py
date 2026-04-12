from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from images.models import Image

CATEGORY_CHOICES = [
    ("painting", "Painting"),
    ("architecture", "Architecture"),
    ("sculpture", "Sculpture"),
    ("photography", "Photography"),
    ("other", "Other"),
]

class ArtPieceBase(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, editable=False)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    images = GenericRelation(Image)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        category = self.__class__.__name__.lower();
        allowed = [choice[0] for choice in CATEGORY_CHOICES]

        if category not in allowed:
            raise ValueError(f"{category} is not a valid category")

        self.category = category
        super().save(*args, **kwargs)

class Painting(ArtPieceBase):
    artist = models.CharField(max_length=100)

class Architecture(ArtPieceBase):
    architect = models.CharField(max_length=100)

class Sculpture(ArtPieceBase):
    artist = models.CharField(max_length=100)

class Photography(ArtPieceBase):
    photographer = models.CharField(max_length=100)

class Other(ArtPieceBase):
    pass

MODEL_MAP = {
    "painting": Painting,
    "architecture": Architecture,
    "sculpture": Sculpture,
    "photography": Photography,
    "other": Other,
}