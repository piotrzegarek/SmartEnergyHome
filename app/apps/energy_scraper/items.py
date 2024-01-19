# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from core.models import EnergyPrice
from scrapy_djangoitem import DjangoItem


class EnergyPriceItem(DjangoItem):
    django_model = EnergyPrice
