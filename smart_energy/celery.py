import os

from celery import Celery
from django.conf import settings

# from celery.schedules import crontab


# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

# from energy_scraper.spiders.energy_spider import EnergySpider


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_energy.settings")

app = Celery("smart_energy")

# config keys has `CELERY` prefix
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     divide.s('Happy Mondays!'),
    # )


# @app.task
# def run_energy_scraper():
#     process = CrawlerProcess(get_project_settings())

#     process.crawl(EnergySpider)
#     process.start()
