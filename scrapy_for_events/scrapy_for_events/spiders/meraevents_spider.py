import scrapy
import math
import array



class QuotesSpider(scrapy.Spider):
    name = "meraevents"

    def start_requests(self):
        urls = [
            'http://www.meraevents.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_events_data)


    def get_events_data(self, response):
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",response.url)
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",response.status)
        total_events=response.css('p.totalCount::text').extract_first()
        max_event=int(total_events)
        max_page=math.ceil(max_event/12) + 1
        print("####################################",type(max_page),"++++",max_page)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2",type(response.body))
        url_list=[]
        for i in range(1 ,max_page):
            url='http://www.meraevents.com/api/event/list?countryId=14&day=6&page=' + str(i) +'&limit=12&eventMode=0'
            # print("222222222222222222222222",i,"33333",url)
            url_list.append(url)
        # print("$$$$$$$$$$$$$$$$$$$$$$4",url_list)

        # print("111111111111111111",url)

        filename = '%s__%s__%s.txt' % ('meraevents', 'url', 'list')

        with open(filename, 'a') as f:
            f.write(',')
            f.write(str(url_list))

        for url in url_list:
            yield scrapy.Request(url=url, callback=self.get_event_price)

    def get_event_price(self,response):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",response.url)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2",response.body)
        print("osdfngiabnfbniub",type((response.body).decode()))
        data=(response.body).decode()
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",data['response'])
        filename = '%s__%s__%s.txt' % ('meraevents', 'price', 'data')

        # with open(filename, 'a') as f:
        #     f.write(',')
        #     f.write(str(data))


