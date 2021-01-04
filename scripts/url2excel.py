import os
import re
import requests
import cssselect
from lxml.html import etree
import json
import urllib.parse
import pandas as pd
from tqdm import tqdm
import time


class URL2Excel():
    def __init__(self):
        self.input_file_name = 'input.txt'
        self.dir = os.path.dirname(__file__)
        self.inpath = os.path.join(self.dir, self.input_file_name)
        self.save_list = []

    def get_url_list(self):
        with open(self.inpath, "r", encoding='utf-8') as f:  # 设置文件对象
            data = f.read()  # 可以是随便对文件的操作
            name_list = re.split(r'\s', data)
        pattern = r'http://tieba.baidu.com/p(.*)'
        self.name_list = [
            item for item in name_list if re.match(pattern, item)]  # 去除空值
        self.name_num = len(self.name_list)
        # print(self.name_list)
        print('valid url:{}'.format(self.name_num))
        return self.name_list

    def process_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        r = requests.get(url, headers=headers)
        html_obj = etree.HTML(r.text)
        
        css = '#j_p_postlist > div:nth-child(1)'
        box = html_obj.cssselect(css)
        if box:
            dict_str = box[0].attrib['data-field']
            content_dict = json.loads(dict_str)
            try:
                comment = content_dict['content']['content'] # 内容
                comment_len = len(comment) # 长度
            except:
                comment = '没有解析出评论'
                comment_len = 0
            params = urllib.parse.urlencode({'wd':comment[:38]},encoding='utf-8')
            search_url = 'https://www.baidu.com/s?{}'.format(params) # 搜索链接
            self.save_list.append({'url':url,'len':comment_len,'content':comment,'search':search_url})
        elif re.match(r'(.*)(很抱歉，您的贴子已被系统删除)(.*)',r.text):
            self.save_list.append({'url':url,'len':'','content':'被系统删帖','search':''})
        elif re.match(r'(.*)(很抱歉，该贴已被删除)(.*)',r.text):
            self.save_list.append({'url':url,'len':'','content':'被贴吧删帖','search':''})
        else:
            self.save_list.append({'url':url,'len':'','content':'没有找到评论内容，可能是链接无效，或程序被ban了','search':''})
        # print(box)
    
    def save(self,filename='out.xlsx'):
        pf = pd.DataFrame(self.save_list)
        outpath = os.path.join(self.dir,filename)
        print('out path:{}'.format(outpath))
        file_path=pd.ExcelWriter(outpath)
        # file_csv_path = pd.read_csv("compound.csv")
        # 替换空单元格
        pf.fillna(' ', inplace=True)
        # 输出
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # pf.to_csv(file_csv_path, encoding='utf-8', index=False)
        # 保存表格
        file_path.save()

    def run(self):
        self.get_url_list()
        for url in tqdm(self.name_list):
            self.process_url(url)
        self.save()


if __name__ == "__main__":
    try:
        u = URL2Excel()
        u.run()
        os.system('pause')
    except:
        time.sleep(10)
        os.system('pause')
