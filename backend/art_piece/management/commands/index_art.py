from django.core.management.base import BaseCommand
from art_piece.services.search_engine.indexing import index_all_art_pieces
from art_piece.services.search_engine.search_engine_service import SearchEngineService

class Command(BaseCommand):
    help = "Indexes all art pieces into the search engine"

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing search engine...")
        engine = SearchEngineService()
        engine.initialize()
        self.stdout.write("Initializing done.")

        self.stdout.write("Indexing all art pieces...")
        index_all_art_pieces()
        self.stdout.write("Indexing done.")