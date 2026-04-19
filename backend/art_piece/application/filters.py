from django.db.models.functions import Lower
from abc import ABC, abstractmethod
from django.http import QueryDict
from ..domain import models
from itertools import chain
from collections import Counter
from commons.search.service import SearchEngineService

def filter_qs_by_field_in_list_ci(qs: QueryDict, field: str, lst: list[str]):
    return qs.annotate(field_lower=Lower(field)).filter(field_lower__in=[l.lower() for l in lst])

class BaseCategoryFilter(ABC):
    """Abstract base filter class for art piece categories, providing common filtering logic."""

    model = None

    def __init__(self, query_params):
        self.query = query_params.get("query")
        self.year = query_params.get("year")
        self.locations = query_params.getlist("locations")
        
    def apply(self, search_ids=None):
        if self.model is None:
            return []

        qs = self.model.objects.prefetch_related("images")

        if search_ids:
            qs = qs.filter(search_id__in=search_ids)

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
    
BASE_CONFIG = {
    "fields": {
        "year": "year",
        "location": "locations"
    }
}

CATEGORY_CONFIG = {
    "painting": {
        "filter": PaintingFilter,
        "fields": {
            "artist": "artists",
            "technique": "techniques", 
            "measurements": "measurements"
        }
    },
    "architecture": {
        "filter": ArchitectureFilter,
        "fields": {
            "architect": "architects"
        }
    },
    "sculpture": {
        "filter": SculptureFilter,
        "fields": {
            "artist": "artists",
            "material": "materials"
        }
    },
    "photography": {
        "filter": PhotographyFilter,
        "fields": {
            "photographer": "photographers",
            "camera": "cameras"
        }
    },
    "other": {
        "filter": OtherFilter,
        "fields": {}
    },
}

# Mapping of category name to its corresponding filter class for easy access in the polymorphic filter
FILTERS_MAP = {k: v["filter"] for k, v in CATEGORY_CONFIG.items()}

# Precompute the set of query parameter names associated with each category for category selection in the polymorphic filter
CATEGORY_PARAMS = {k: set(v["fields"].values()) for k, v in CATEGORY_CONFIG.items()}

class ArtPiecePolymorphicFilter:
    """Polymorphic filter that applies the appropriate category filter based on query parameters."""

    def __init__(self, query_params):
        self.query_params = query_params

    def _select_categories(self):
        """Determine which categories to filter based on the presence of category-specific query parameters."""
        selected = set()

        query_categories = self.query_params.getlist("categories")

        if query_categories:
            for category in query_categories:
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
    
    def _search(self) -> list[int]:
        """Perform a search and return a list of search ids."""
        search_ids = []

        query = self.query_params.get("query")

        if not query or query.strip() == "":
            return search_ids

        engine = SearchEngineService()

        hits = engine.search(query)["hits"]
        search_ids = [hit["id"] for hit in hits]

        return search_ids
        
    def _build_meta(self, querysets: list):
        """Build metadata for the filtered results, including counts of unique values for each filterable field."""
        meta = {}
        categories = []

        for qs in querysets:
            if not qs.exists():
                continue

            model_name = qs.model.__name__.lower()

            categories.extend([v.category for v in qs])

            fields = {**BASE_CONFIG["fields"], **CATEGORY_CONFIG[model_name]["fields"]}

            for db_field, param_name in fields.items():
                values = list(qs.values_list(db_field, flat=True))

                values = [v for v in values if v is not None and v != ""]

                if len(values) == 0:
                    continue

                if param_name not in meta:
                    meta[param_name] = Counter()

                meta[param_name].update(values)

        meta["categories"] = Counter(categories)
        return {k: dict(v.most_common()) for k, v in meta.items()}

    def apply(self):
        """Apply the appropriate filters based on query parameters and return the filtered results."""
        querysets = []

        selected = self._select_categories()
        search_ids = self._search()

        for category, filter_class in FILTERS_MAP.items():
            if category in selected:
                querysets.append(filter_class(self.query_params).apply(search_ids))
        
        meta = self._build_meta(querysets)
        results = list(chain(*querysets))

        return results, meta