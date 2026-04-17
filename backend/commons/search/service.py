from dataclasses import dataclass
from django.conf import settings
import requests
import logging
import uuid

logger = logging.getLogger(__name__)

@dataclass
class IndexItem:
    "Data class representing an item to be indexed in the search engine."
    id: uuid.UUID
    title: str
    description: str
    tags: list[str]

class SearchEngineService:
    """Service class for interacting with the search engine, including indexing items and performing search queries."""
    def __init__(self):
        self.base_url = settings.SEARCH_ENGINE_URL
        self.timeout = 5

    def initialize(self):
        index_options = {
            "useOwnIds": True
        }

        response = requests.post(
            f"{self.base_url}/engine/init",
            json=index_options,
            timeout=self.timeout
        )

        response.raise_for_status()
        return response.json()

    def index_item(self, item: IndexItem):
        item = {
            "id": str(item.id),
            "title": item.title,
            "description": item.description,
            "tags": item.tags
        }

        response = requests.post(
            f"{self.base_url}/documents",
            json=item,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        return response.json()

    def index_items_bulk(self, items: list[IndexItem]):
        """Index a list of items in bulk by sending them to the search engine's bulk indexing endpoint."""
        items_json = []

        for item in items:
            items_json.append(
                {
                    "id": str(item.id),
                    "title": item.title,
                    "description": item.description,
                    "tags": item.tags
                }
            )             

        response = requests.post(
            f"{self.base_url}/documents/bulk",
            json=items_json,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def update_item(self, item: IndexItem):
        payload = {
            "title": item.title,
            "description": item.description,
            "tags": item.tags
        }       

        response = requests.patch(
            f"{self.base_url}/documents/{str(item.id)}",
            json=payload,
            timeout=self.timeout
        )

        print(response.text)

        response.raise_for_status()
    
    def delete_item(self, id: str | uuid.UUID):
        response = requests.delete(
            f"{self.base_url}/documents/{str(id)}",
            timeout=self.timeout
        )

        response.raise_for_status()

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