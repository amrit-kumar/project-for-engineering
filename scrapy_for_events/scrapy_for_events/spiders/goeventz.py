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
    name = "goeventz"

    def start_requests(self):
        urls = [
            'https://www.goeventz.com/',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_each_page_url)


    def get_each_page_url(self, response):
        # var1=HtmlResponse(url='https://www.goeventz.com/')
        var2=response.css('li.unavailable')
        href=var2.css('a::attr(href)').extract_first()
        max_page_no=int(href.split('=')[1])
        base_url='https://www.goeventz.com/?page='
        for i in range(max_page_no):
            url=base_url + str(i)
            # print("111111111111111111",url)

            filename = '%s__%s__%s.txt' % ('goeventz', 'url', 'list')

            # with open(filename, 'a') as f:
            #     f.write(',')
            #     f.write(str(var3))
            # print("!!!!!!!!!!!!!!!!!!!!!!!!!!",len(var3),"urllll",response.url)
            #
            yield scrapy.Request(url=url,callback=self.get_href_for_each_event)


    def get_href_for_each_event(self,response):

        filename = '%s__%s__%s.txt' % ('goeventz', 'events', 'urllist')
        var=response.css('div.list_detail')
        # print("22222222222222222",response.url)
        # print("33333333333333333",len(var))
        for i in var:

            href=i.css('a::attr(href)').extract_first()
            # print("44444444444444444444",href)

            yield scrapy.Request(url=href,callback=self.get_event_price)

    def get_event_price(self,response):

        # print("555555555555555555555",response.url)
        g_dict={}
        filename = '%s__%s__%s.txt' % ('goeventz', 'events', 'pricedata')
        urlfile = '%s__%s__%s.txt' % ('goeventz', 'price', 'empty')

        event_name=response.css('h3::text').extract_first()
        my_list=[]
        g_dict['event_name']=event_name
        my_list.append(g_dict)
        var2=response.css('div.event_ticket_container')
        var3=var2.css('div.event_ticket')
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@",response.url)
        # print("66666666666666666",len(var3.extract()))
        if len(var3.extract())==0:
            with open(urlfile, 'a') as f:
                f.write(',')
                print("#########################",response.url)
                f.write(response.url)
        t_dict = {}
        e_list=[]
        for i in var3:
            p_dict = {}
            ticket_type = i.css('h4.ticket_name::text').extract()
            prices = i.css('div.currancy_e::text').extract()
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!',prices)

            if len(prices)==0 or len(ticket_type)==0:
                ticket_type='empty'
                price='empty'
            else:
                ticket_type = ticket_type[0]
                price = prices[0]
            # print('121211212121212121',ticket_type,'5656565656565656',price)
            # print("################3#####",response.url)
            pric=price.strip(' \t\n\r').replace(" ", "").replace("\n", "")
            p_dict['ticket_type']=ticket_type
            p_dict['price']=pric

            # print("66666666666666666666",pric)
            # p_dict.update({ticket_type:pric})
            # t_dict.update({"event_data":p_dict})
            # print("111111111111111111111111111111",my_list)
            e_list.append(p_dict)
            # print("22222222222222222222222222",e_list)
        # print("00000000000000000000000000000", e_list)

        t_dict['event_data']=e_list
        my_list.append(t_dict)
        # print("3333333333333333333333333",my_list)
        with open(filename, 'a') as f:
            f.write(',')
            f.write(str(my_list))
        # if not event_name:
        #     print("!!!!!!!!!!!!!!!!!!!!!!!!!",response.url)
        # print("22222222222222222222",event_name)



