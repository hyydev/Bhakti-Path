
from django.core.management.base import BaseCommand
from apps.ProductsManagement.scrapers.mayapuri_scraper import MayapuriScraper

class Command(BaseCommand):
    help = "Run all scrapers"

    def handle(self, *args, **kwargs):
        scraper = MayapuriScraper()
        scraper.scrape()
        scraper.close()