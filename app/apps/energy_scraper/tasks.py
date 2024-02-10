from celery import shared_task
from django.apps import apps
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


@shared_task
def run_energy_scraper():
    print("Running energy spider...")
    # Ensure Django is properly configured before importing models
    if not apps.ready:
        from django.core.management import call_command

        call_command("migrate")

    process = CrawlerProcess(get_project_settings())
    process.crawl("energy")

    process.start()
