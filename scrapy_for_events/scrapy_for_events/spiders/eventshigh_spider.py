import scrapy
import array
# import libxml2
import json
from pprint import pprint
from scrapy.linkextractors import LinkExtractor
from collections import Counter
from lxml import html
import requests
import webbrowser
from lxml.html.soupparser import fromstring
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.spiders.feed import XMLFeedSpider, CSVFeedSpider
from scrapy.spiders.sitemap import SitemapSpider

class QuotesSpider(scrapy.Spider):
    name = "eventshigh"

    def start_requests(self):
        urls = [
            'https://www.eventshigh.com/city/Bangalore',
            'https://www.eventshigh.com/city/Chennai',
            'https://www.eventshigh.com/city/Delhi',
            'https://www.eventshigh.com/city/Mumbai',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        var3=response.css('a::attr(href)').extract()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!",response.url)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@",var3)

        page = response.url.split("/")[-2]
        for i in var3:

            if "https" in i:
                print("$$$$$$$$$$$$$$$$$",i.split())

            slicee='https://www.eventshigh.com'+i
            print("##########################",slicee)

        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)