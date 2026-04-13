from django.db.models.functions import Cast, Lower
from abc import ABC, abstractmethod
from django.http import QueryDict
from . import models

def filter_qs_by_field_in_list_ci(qs: QueryDict, field: str, lst: list[str]):
    return qs.annotate(field_lower=Lower(field)).filter(field_lower__in=[l.lower() for l in lst])

class BaseCategoryFilter(ABC):
    """Abstract base filter class for art piece categories, providing common filtering logic."""

    model = None

    def __init__(self, query_params):
        self.year = query_params.get("year")
        self.locations = query_params.getlist("locations")
        
    def apply(self):
        if self.model is None:
            return []

        qs = self.model.objects.prefetch_related("images")
        qs = self._apply_base_filters(qs)
        qs = self._apply_category_filters(qs)
        return qs
    
    def _apply_base_filters(self, qs):
        if self.year:
            qs = qs.filter(year=self.year)
        if self.locations:
            qs = filter_qs_by_field_in_list_ci(qs, "location", self.locations)
        return qs

    @abstractmethod          
    def _apply_category_filters(self, qs):
        pass

class PaintingFilter(BaseCategoryFilter):
    """Filter class for paintings, extending the base category filter with painting-specific filters."""

    model = models.Painting

    def __init__(self, query_params):
        super().__init__(query_params)
        self.artists = query_params.getlist("artists")
        self.techniques = query_params.getlist("techniques")
        self.measurements = query_params.getlist("measurements")
    
    def _apply_category_filters(self, qs):
        if self.artists:
            qs = filter_qs_by_field_in_list_ci(qs, "artist", self.artists)  

        if self.techniques:
            qs = filter_qs_by_field_in_list_ci(qs, "technique", self.techniques) 

        if self.measurements:
            qs = filter_qs_by_field_in_list_ci(qs, "measurements", self.measurements)           

        return qs    

class ArchitectureFilter(BaseCategoryFilter):
    """Filter class for architecture, extending the base category filter with architecture-specific filters."""

    model = models.Architecture

    def __init__(self, query_params):
        super().__init__(query_params)
        self.architects = query_params.getlist("architects")
    
    def _apply_category_filters(self, qs):
        if self.architects:
            qs = filter_qs_by_field_in_list_ci(qs, "architect", self.architects)  

        return qs        

class SculptureFilter(BaseCategoryFilter):
    """Filter class for sculpture, extending the base category filter with sculpture-specific filters."""

    model = models.Sculpture

    def __init__(self, query_params):
        super().__init__(query_params)
        self.artists = query_params.getlist("artists")
        self.materials = query_params.getlist("materials")
    
    def _apply_category_filters(self, qs):
        if self.artists:
            qs = filter_qs_by_field_in_list_ci(qs, "artist", self.artists)  

        if self.materials:
            qs = filter_qs_by_field_in_list_ci(qs, "material", self.materials) 

        return qs    

class PhotographyFilter(BaseCategoryFilter):
    """Filter class for photography, extending the base category filter with photography-specific filters."""

    model = models.Photography

    def __init__(self, query_params):
        super().__init__(query_params)
        self.photographers = query_params.getlist("photographers")
        self.cameras = query_params.getlist("cameras")
    
    def _apply_category_filters(self, qs):
        if self.photographers:
            qs = filter_qs_by_field_in_list_ci(qs, "photographer", self.photographers)  

        if self.cameras:
            qs = filter_qs_by_field_in_list_ci(qs, "camera", self.cameras) 

        return qs    

class OtherFilter(BaseCategoryFilter):
    """Filter class for other category, extending the base category filter without additional filters."""

    model = models.Other

    def __init__(self, query_params):
        super().__init__(query_params)
    
    def _apply_category_filters(self, qs):
        return qs

FILTERS_MAP = {
    "painting": PaintingFilter,
    "architecture": ArchitectureFilter,
    "sculpture": SculptureFilter,
    "photography": PhotographyFilter,
    "other": OtherFilter    
}

CATEGORY_PARAMS = {
    "painting": {"artists", "techniques", "measurements"},
    "architecture": {"architects"},
    "sculpture": {"artists", "materials"},
    "photography": {"photographers", "cameras"},
    "other": set(),
}

class ArtPiecePolymorphicFilter:
    """Polymorphic filter that applies the appropriate category filter based on query parameters."""

    def __init__(self, query_params):
        self.query_params = query_params

    def _selected_categories(self):
        """Determine which categories to filter based on the presence of category-specific query parameters."""
        selected = set()

        query_categories = self.query_params.getlist("categories")

        if query_categories:
            for category in query_categories:
                print(category)
                if category not in FILTERS_MAP.keys():
                    raise ValueError(f"Unknown category: {category}")
                
                if category in FILTERS_MAP:
                    selected.add(category)
        else:
            for category, params in CATEGORY_PARAMS.items():
                if any(self.query_params.getlist(p) for p in params):
                    selected.add(category)

        # If no category-specific parameters are present, select all categories by default
        if not selected:
            selected = set(FILTERS_MAP.keys())

        return selected

    def apply(self):
        results = []
        selected = self._selected_categories()

        for category, filter_class in FILTERS_MAP.items():
            if category in selected:
                results.extend(list(filter_class(self.query_params).apply()))
        return results