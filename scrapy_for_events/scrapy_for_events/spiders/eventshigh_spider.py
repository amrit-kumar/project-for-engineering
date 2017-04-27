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
from scrapy.loader.processors import MapCompose
import re


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
            yield scrapy.Request(url=url, callback=self.parse_duration)


    def parse_duration(self, response):
        var1=response.css('div.margin-top15')
        var3=var1.css('a::attr(href)').extract()
        filename = '%s__%s__%s.txt' % ('eventshigh', 'city', 'event1')
        with open(filename, 'a') as f:
            f.write(',')
            f.write(str(var3))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!",len(var3),"urllll",response.url)

        # page = response.url.split("/")[-2]
        # list1=[]
        filename = '%s__%s__%s.txt' % ('eventshigh', 'url', 'event2')


        for i in var3:
            a=['http','#']
            # slicee=''
            if not any(x in i for x in a):
                slicee='https://www.eventshigh.com'+i

                with open(filename, 'a') as f:
                    f.write(',')
                    f.write(str(slicee))

            # print("##########################",slicee)

                yield scrapy.Request(url=slicee,callback=self.parse_price)


    def parse_price(self,response):

        filename = '%s__%s__%s.txt' % ('eventshigh', 'price', 'data3')

        var=response.css('div.ecbox-polaroid')
        for i in var:

            event_name=i.css('h3::text').extract()
            price=i.css('div.browse-price-wrp::text').extract()
            # print("&&&&&&&&&&&&&&&&&&&&&",price)

            with open(filename, 'a') as f:

                f.write('|||')
                f.write(str(event_name))
                f.write(':')
                string=price[0]
                string=string.rstrip('\n')
                print("11111111111111111111111", string,"222222222222222222222",response.url,"333333333333333333333333",event_name)

                f.write(string)

        # price=var.css('div.browse-price-wrp::text').re(r'Rs*')
        # print("****************************",price)
        yield scrapy.Request(url=response.url)



