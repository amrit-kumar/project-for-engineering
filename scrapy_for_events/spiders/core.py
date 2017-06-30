import os

import django

from scrapy_for_events.spiders import bookmyshow_spider

# scrapy api
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.settings import Settings


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consultad.settings')
# django.setup()
#
# def spider_closing(spider):
#     """Activates on spider closed signal"""
#     log.msg("Closing reactor", level=log.INFO)
#     reactor.stop()
# #
# # log.start(loglevel=log.DEBUG)
# settings = Settings()
#
# # crawl responsibly
# # settings.set("USER_AGENT", "consultad.setting")
# crawler = Crawler(settings)
#
# # stop reactor when spider closes
# crawler.signals.connect(spider_closing, signal=signals.spider_closed)
#
# crawler.configure()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(bookmyshow_spider)


# crawler.crawl(DmozSpider())
process.start()
# reactor.run()