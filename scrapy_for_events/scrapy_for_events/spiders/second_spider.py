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


class BookMyShowSpider(scrapy.Spider):
    name = "bookmyshow"

    def start_requests(self):
        urls=[]
        with open('bookmyshow_regionlist.json') as data_file:
            data = json.load(data_file)
            for i in data.values():
                for j in i:
                    city_names=j['name'].lower()
                    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", city_names)

                    var=city_names
                    t_url= 'https://in.bookmyshow.com/'+ var +'/events'
                    urls.append(t_url)
        # var='pune'
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@", urls)
        # urls = [
        #     'https://in.bookmyshow.com/'+ 'pune' +'/events',
        #     'https://in.bookmyshow.com/'+ 'mumbai' +'/events',
        # ]
        for url in urls:

            yield scrapy.Request(url=url, callback=self.parse)
            # yield scrapy.Request(url=slicee, callback = lambda r: self.parse_price(r))



    def parse(self, response):

        # print("#########################",response.url)
        c_dict={}
        e_dict={}
        tag=response.css('div.ev-card')
        city=response.url.split("/")[3]

        # print("TTTTTTTTTTTTTTTTTTTT",tag)
        for i in tag:

            events=i.css('a::attr(title)').extract_first()
            prices=i.css('span.__price::text').extract_first()

            # print("events==========================",events)
            # print("price+++++++++++++++++++++++++ ",prices)
        # for i,j in zip(events,prices):
            e_dict.update({events:prices})

        # print("eeeeeeeeeeeeeeeeeeeeeeeeeeeee",e_dict)
        c_dict[city]=e_dict
        filename = '%s__%s__%s.txt' % ('bookmyshow', 'city', 'event3')
        with open(filename, 'a') as f:
            f.write(',')
            f.write(str(c_dict))

        var=response.css('div.buy-now')
        var3=var.css('a::attr(href)').extract()
        list1=[]
        for i in var3:

            slicee='https://in.bookmyshow.com'+i
            list1.append(slicee)
            # slicee='https://in.bookmyshow.com/pune/events/lilly-singh-how-to-be-a-bawse/ET00054303'
            next_page = response.urljoin(slicee)
            yield scrapy.Request(url=slicee,callback=self.parse_price)
            # print("5555555555555555555555555555",list1)
        # yield scrapy.Request(url=list1[0], callback=self.parse_price)

        # print("111111111111111111111", i.split("/"))

    def parse_price(self,response):
        p_dict={}
        c_dict = {}
        e_dict = {}
        # print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ",response.url)
        website = response.url.split("/")[2].split(".")[1]
        # print(website)
        city=response.url.split("/")[3]
        # print(city)
        event=response.url.split("/")[-2]
        # print("event----name ", event)

        # data2=response.css('div.__price')
        # print("333333333333333333333333",data2)
        # data3=data2.css('span::text').extract()
        # print("44444444444444444444444",data3)

        # data4=response.css('div.f50')
        # data5=data4.css('div.tktDiv')
        n_list=[]
        data6=response.css('div.tktCat')
        data7=data6.css('span *::text').extract() #will get all text in span tag
        # print("55555555555555555555555",data7)
        # p_data=data7
        if not data7:
            # n_list.append(response.url)
            # print("@@@@@@@@@@@@@@@@@@@@@@@@",n_list)


            data8=response.css('div.bookDv').extract()
            data8=response.css('div.price *::text').extract()
            # data9=data8.css('div.fc-content').extract()
            # print("666666666666666666666666",data8)
            # p_data=data8
            if not data8:
                data = response.css('div.ticket-container')
                # print("111111111111111111111", data)
                data1 = data.css('div.regBk').extract()
                print("22222222222222222222", data1)
                # p_data=data1
                if not data1:
                    print("!!!!!!!!!!!!!!!!!!!!!!", response.url)
                    p_data = response.url

                    filename = '%s__%s.txt' % ('bookmyshow', 'price')
                    print("##################",p_data)
                    with open(filename, 'a') as f:
                        p_dict.update({event: p_data})
                        f.write(str(p_dict))





                    # hi = response.css('newBtn.p').extract()
        # by=response.css('tktCat.span::text').re(r'Rs.*')
        #
        # by=response.css('div.price-details::text').re(r'Rs.*')
        # print("@@@@@@@@@@@@@@@@@@@@@@@@22",type(by))
        # if by:
        # print("333333333333333333333333", "price", hi,"444444444444444444444",by)


            # f.write(str(p_dict))
            # json.dump(p_dict,f)
            # f.write(",".join(str(p_list)))
            # print("*****************",filename)

