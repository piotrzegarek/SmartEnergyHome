# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem

from app.apps.core.models import EnergyPrice


class EnergyPriceItem(DjangoItem):
    django_model = EnergyPrice
