from dataclasses import dataclass
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

@dataclass
class IndexItem:
    id: int
    title: str
    description: str
    tags: list[str]

class SearchEngineService:
    def __init__(self):
        self.base_url = settings.SEARCH_ENGINE_URL
        self.timeout = 5

    def index_items_bulk(self, items: list[IndexItem]):
        items_json = []

        for item in items:
            items_json.append(
                {
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

    def search(self, query: str):
        params = {"query": query}

        response = requests.get(
            f"{self.base_url}/search",
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        logger.info("search response: %s", response.text)
        return response.json()