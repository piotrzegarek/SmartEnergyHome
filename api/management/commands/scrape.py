from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from energy_scraper.spiders.energy_spider import EnergySpider


class Command(BaseCommand):
    help = "Scrape the energy prices"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        process.crawl(EnergySpider)
        process.start()
