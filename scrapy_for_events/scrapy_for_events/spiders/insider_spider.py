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
    name = "insider"

    def start_requests(self):
        urls = [
        'https://insider.in/bangalore','https://insider.in/delhi','https://insider.in/mumbai',
        'https://insider.in/pune','https://insider.in/ahmedabad','https://insider.in/chandigarh',
        'https://insider.in/chennai','https://insider.in/goa','https://insider.in/guwahati',
        'https://insider.in/hyderabad','https://insider.in/jaipur','https://insider.in/kochi',

        'https://insider.in/kolkata','https://insider.in/ludhiana','https://insider.in/vadodara',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_events_data)


    def get_events_data(self, response):

        list_u=['?view=Events','?view=Food','?view=Travel','?view=Workshops','?view=Long+Weekend']
        url_list=[]
        for i in list_u:
            url_list.append(response.url + i)
        print("$$$$$$$$$$$$$$$$$$$$$$4",url_list)

        # print("111111111111111111",url)

        filename = '%s__%s__%s.txt' % ('goeventz', 'url', 'list')

        # with open(filename, 'a') as f:
        #     f.write(',')
        #     f.write(str(var3))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!",len(var3),"urllll",response.url)
        #
        # yield scrapy.Request(url=url,callback=self.get_href_for_each_event)
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.get_event_price)



    #
    # def get_href_for_each_event(self,response):
    #
    #     filename = '%s__%s__%s.txt' % ('goeventz', 'events', 'urllist')
    #     var=response.css('div.list_detail')
    #     # print("22222222222222222",response.url)
    #     # print("33333333333333333",len(var))
    #     for i in var:
    #
    #         href=i.css('a::attr(href)').extract_first()
    #         # print("44444444444444444444",href)
    #
    #         yield scrapy.Request(url=href,callback=self.get_event_price)

    def get_event_price(self,response):
        #todo remove data redundancy
        print("@@@@@@@@@@@@@@@@@@", response.url)
        filename = '%s__%s__%s.txt' % ('insider', 'events', 'pricedata')

        var = response.css('li.card-list-item')
        t_dict={}
        e_dict={}
        for i in var:
            e_dict['event-name']=i.css('div.event-card-name *::text').extract()
            e_dict['event-date'] =i.css('span.event-card-date::text').extract()
            e_dict['event-venue'] =i.css('span.event-card-venue::text').extract()
            e_dict['event-price'] =i.css('span.event-card-price::text').extract()
        t_dict['event_data']=e_dict
        print("1111111111111111111111111111",t_dict)


        with open(filename, 'a') as f:
            f.write(',')
            f.write(str(t_dict))

        var2=var.css('h3::text').extract()
        print("#######################", len(var.extract()))
        print("% %%%%%%%%%%%%%%%%%%%%%%%%%",var2)


        # print("555555555555555555555",response.url)



