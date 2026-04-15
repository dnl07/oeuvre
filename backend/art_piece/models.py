from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from images.models import Image
from django.utils.text import slugify
from .validators import validate_year, validate_measurements
from .normalize import normalize_name, normalize_sentence

CATEGORY_CHOICES = [
    ("painting", "Painting"),
    ("architecture", "Architecture"),
    ("sculpture", "Sculpture"),
    ("photography", "Photography"),
    ("other", "Other"),
]

class ArtPieceBase(models.Model):
    """Abstract base model for art pieces with common fields and logic."""

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, editable=False)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=14, blank=True, null=True, validators=[validate_year])

    images = GenericRelation(Image)

    NORMALIZE_NAME_FIELDS = []
    NORMALIZE_SENTENCE_FIELDS = ["location"]

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Automatically set the category based on the model name
        category = self.__class__.__name__.lower();
        allowed = [choice[0] for choice in CATEGORY_CHOICES]

        if category not in allowed:
            raise ValueError(f"{category} is not a valid category")

        self.category = category

        if not self.slug or not self.slug.startswith(slugify(self.title)):
            self.slug = slugify(self.title)
            unique_slug = self.slug
            counter = 1

            while MODEL_MAP.get(self.category).objects.filter(slug=self.slug).exists():
                self.slug = f"{unique_slug}-{counter}"
                counter += 1

        for field in self.NORMALIZE_NAME_FIELDS:
            value = getattr(self, field, None)
            setattr(self, field, normalize_name(value))

        for field in self.NORMALIZE_SENTENCE_FIELDS:
            value = getattr(self, field, None)
            setattr(self, field, normalize_sentence(value))

        super().save(*args, **kwargs)

class Painting(ArtPieceBase):
    artist = models.CharField(max_length=255, blank=True, null=True)
    technique = models.CharField(max_length=255, blank=True, null=True)
    measurements = models.CharField(max_length=255, blank=True, null=True, validators=[validate_measurements])

    NORMALIZE_NAME_FIELDS = ["artist"]
    NORMALIZE_SENTENCE_FIELDS = ["technique"] + ArtPieceBase.NORMALIZE_SENTENCE_FIELDS

class Architecture(ArtPieceBase):
    architect = models.CharField(max_length=255, blank=True, null=True)

    NORMALIZE_NAME_FIELDS = ["architect"]

class Sculpture(ArtPieceBase):
    artist = models.CharField(max_length=255, blank=True, null=True)
    material = models.CharField(max_length=255, blank=True, null=True)

    NORMALIZE_NAME_FIELDS = ["artist"]
    NORMALIZE_SENTENCE_FIELDS = ["material"] + ArtPieceBase.NORMALIZE_SENTENCE_FIELDS

class Photography(ArtPieceBase):
    photographer = models.CharField(max_length=255, blank=True, null=True)
    camera = models.CharField(max_length=255, blank=True, null=True)

    NORMALIZE_NAME_FIELDS = ["photographer"]
    NORMALIZE_SENTENCE_FIELDS = ["camera"] + ArtPieceBase.NORMALIZE_SENTENCE_FIELDS

class Other(ArtPieceBase):
    pass

MODEL_MAP = {
    "painting": Painting,
    "architecture": Architecture,
    "sculpture": Sculpture,
    "photography": Photography,
    "other": Other,
}