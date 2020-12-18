from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request

import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from items import PhoneCommentItem,PhoneScoreItem

sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
from utils.mysqlservice import MySQLService

class CommentSpdier(Spider):
    name = 'CommentSpdier'
    def __init__(self):
        super().__init__()
        self.ce = MySQLService()

    def start_requests(self):
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

        name_url_list = self.ce.select(table='t_phone_comment_url',field=['name','url'])
        for item in name_url_list:
            name = item['name']
            url = item['url']
            yield Request(url=url,headers=headers,meta={'name':name},callback=self.parse_information)

    def parse_information(self,response):
        name = response.meta['name']
        comment_item = self.comment_item_init()
        if not response.css("div.main > div.col-ab > div.area.area-total-score > div").extract():
            # 用一个元素判断这个页面对不对
            return 

        comment_item['name'] = name
        comment_box = response.css('#JcmtList > ul > li > dl>dd.cmt-detail>div>ul')
        for comment in comment_box:
            comment_list = comment.css('li::text').extract()
            tag_list = comment.css('li>span::text').extract()
            for tag, comment in zip(tag_list,comment_list):
                if '最满意' in tag:
                    comment_item['like'] = comment
                if '最不满意' in tag:
                    comment_item['dislike'] = comment
                if '做工外观' in tag:
                    comment_item['appearance'] = comment
                if '配置性能' in tag:
                    comment_item['performance'] = comment
                if '系统流畅度' in tag:
                    comment_item['fluency'] = comment 
                if '拍照效果' in tag:
                    comment_item['camera'] = comment 
                if '其它描述' in tag:
                    comment_item['other'] = comment
            yield comment_item

        score_item = self.score_item_init()
        score_item['name'] = name
        score_item['score'] = response.css('#Jwrap > div.main > div.col-ab > div.area.area-total-score > div > div.circle.circle-200 > div.c-in > strong::text').extract_first()
        
        score_box = response.css('#Jwrap > div.main > div.col-ab > div.area.area-total-score > div > div.total-com > table')
        score_info_list = score_box.css('tr>td::text').extract()
        score_info_list = [item for item in score_info_list if re.match(r'.*：\d\.\d',item)]
        for item in score_info_list:
            if '性价比' in item:
                score_item['cheap'] = item[-3:]
            if '屏幕显示' in item:
                score_item['display'] = item[-3:]
            if '流畅度' in item:
                score_item['fluency'] = item[-3:]
            if '电池与续航' in item:
                score_item['battery'] = item[-3:]
            if '拍照效果' in item:
                score_item['camera'] = item[-3:]    

        yield score_item  # 把取到的数据提交给pipline处理

    def comment_item_init(self):
        item = PhoneCommentItem()
        item['name'] = ''
        item['like'] = ''
        item['dislike'] = ''
        item['appearance'] = ''
        item['performance'] = ''
        item['fluency'] = ''
        item['camera'] = ''
        item['other'] = ''
        return item

    def score_item_init(self):
        item = PhoneScoreItem()
        item['name'] = ''
        item['score'] = ''
        item['cheap'] = ''
        item['display'] = ''
        item['fluency'] = ''
        item['battery'] = ''
        item['camera'] = ''
        return item

