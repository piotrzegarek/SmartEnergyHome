from celery import shared_task
from django.apps import apps
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# @shared_task
# def run_energy_scraper():
#     print("elo")
#     call_command("run_scraper", )


@shared_task
def run_energy_scraper():
    # Ensure Django is properly configured before importing models
    print("Running energy spider...")
    if not apps.ready:
        from django.core.management import call_command

        call_command("migrate")

    # from .spiders.energy_spider import EnergySpider

    process = CrawlerProcess(get_project_settings())
    process.crawl("energy")
    print("Start...")

    process.start()
