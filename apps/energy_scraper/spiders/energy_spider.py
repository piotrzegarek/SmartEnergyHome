import os

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_splash import SplashRequest

from ..items import EnergyPriceItem


class EnergySpider(scrapy.Spider):
    name = "energy"

    def start_requests(self):
        url = os.getenv("SCRAP_URL")

        if url:
            yield SplashRequest(url=url, callback=self.parse, args={"wait": 20})
        else:
            raise CloseSpider("No URL provided.")

    def parse(self, response):
        date = (
            response.xpath(
                '//p/strong[text()="Doba handlowa:"]/following-sibling::text()[1]'
            )
            .get()
            .strip()
        )

        for hour in range(1, 25):
            price = response.xpath(
                f'//tr[td[1]/div/text()="{hour}"]/td[2]/div/text()'
            ).get()
            price = price.replace(",", ".")
            item = EnergyPriceItem(date=date, hour=hour, price=float(price))

            yield item
