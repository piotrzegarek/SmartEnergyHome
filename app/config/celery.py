import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from app.apps.energy_scraper.tasks import run_energy_scraper

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config.settings")

app = Celery("config")

# config keys has `CELERY` prefix
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    worker_max_tasks_per_child=1, broker_pool_limit=None, timezone=settings.TIME_ZONE
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=1), run_energy_scraper.s(), name="Scrape energy prices"
    )
