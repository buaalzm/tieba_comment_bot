from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request

import sys
import os
import urllib.parse

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from items import PhoneCommentUrlItem

sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
from utils.fileloader import FileLoader
from utils.mysqlservice import MySQLService



class url_get(Spider):
    name = "url_get"
    def __init__(self):
        super().__init__()
        self.ce = MySQLService()

    def start_requests(self):
        fl = FileLoader()
        fl.loadfile('phone.txt')
        namelist = fl.get_name_list()
        # print(namelist)
        headers = {
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9',
            'cookie':'abuid=wKjvh1/TJtiosEG7Dq0kAg==; JSESSIONID=abcion8Q4mQyyf247Zqzx; uComment=fc7ac69c; captcha=943bf15dd76b9c60-56457dc1764c8a8e1d54bb267604373587686364',
            'referer':'https://ks.pconline.com.cn/index.shtml?q=iphone8plus&scope=',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'same-origin',
            'sec-fetch-user':'?1',
            'upgrade-insecure-requests':1,
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        for name in namelist:
            if self.ce.check_exists(table='t_phone_comment_url',field='name',value=name):
                continue
            params = urllib.parse.urlencode({'q':name},encoding='gb2312')
            url = "https://ks.pconline.com.cn/index.shtml?{}".format(params)
            yield Request(url=url,headers=headers,meta={'name':name},callback=self.parse_information)

    def parse_information(self,response):
        item = PhoneCommentUrlItem()
        if not response.css("dd.inlet > a:nth-child(1)::attr(href)").extract():
            return 
        url = 'https:'+response.css("dd.inlet > a:nth-child(1)::attr(href)").extract()[0]
        item['name'] = response.meta['name']
        item['url'] = url
        yield item  # 把取到的数据提交给pipline处理
