from dataclasses import dataclass
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

@dataclass
class IndexItem:
    "Data class representing an item to be indexed in the search engine."
    id: int
    title: str
    description: str
    tags: list[str]
    metadata: dict[str, str]

class SearchEngineService:
    """Service class for interacting with the search engine, including indexing items and performing search queries."""
    def __init__(self):
        self.base_url = settings.SEARCH_ENGINE_URL
        self.timeout = 5

    def index_items_bulk(self, items: list[IndexItem]):
        """Index a list of items in bulk by sending them to the search engine's bulk indexing endpoint."""
        items_json = []

        for item in items:
            items_json.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "tags": item.tags,
                    "metadata": item.metadata
                }
            )             

        response = requests.post(
            f"{self.base_url}/documents/bulk",
            json=items_json,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def search(self, query: str):
        """Perform a search query against the search engine and return the results."""
        params = {"query": query}

        response = requests.get(
            f"{self.base_url}/search",
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()