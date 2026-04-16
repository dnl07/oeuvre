from django.core.management.base import BaseCommand
from art_piece.services.search_engine.indexing import index_all_art_pieces


class Command(BaseCommand):
    help = "Indexes all art pieces into the search engine"

    def handle(self, *args, **kwargs):
        self.stdout.write("Indexing all art pieces...")
        index_all_art_pieces()
        self.stdout.write("Indexing done.")