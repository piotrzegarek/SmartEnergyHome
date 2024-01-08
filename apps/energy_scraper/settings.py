# Scrapy settings for energy_scraper project

BOT_NAME = "energy_scraper"

SPIDER_MODULES = ["energy_scraper.spiders"]
NEWSPIDER_MODULE = "energy_scraper.spiders"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Splash Server Endpoint
SPLASH_URL = "http://splash:8050"

# Enable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}

# Enable spider middlewares
SPIDER_MIDDLEWARES = {
    "scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
}

DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"

# Configure item pipelines
ITEM_PIPELINES = {
    "energy_scraper.pipelines.EnergyScraperPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
