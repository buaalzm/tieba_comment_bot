"""
清理被删除的帖子
"""

import sys
import os
import re
import requests
from tqdm import tqdm
import time
from selenium import webdriver

sys.path.append(os.path.dirname(__file__))

class UrlFilter():
    def __init__(self,method='requests'):
        self.filedir = os.path.join(os.path.dirname(__file__),'../','out')
        self.deldir = os.path.join(os.path.dirname(__file__),'../','del')
        self.black_list = []
        self.method = method
        if self.method=='selenium':
            option = webdriver.ChromeOptions()
            # option.add_argument('headless') # 设置option
            self.driver = webdriver.Chrome(options=option)

    def __del__(self):
        if self.method=='selenium':
            self.driver.quit()

    def get_url_list(self,filename):
        """
        提取出文件中已经弄完的项
        目录不存在返回空列表
        params:
        {
            filename[str]:绝对路径
        }
        return [[name,url],]
        """
        ret = []
        if not os.path.exists(filename):
            return []
        with open(filename,'r',encoding='utf-8') as f:
            for line in f:
                spt = line.split(' ')
                ret.append([' '.join(spt[0:-1]),spt[-1]])
        return ret

    def get_file_list(self):
        filelist = os.listdir(self.filedir)
        return [item for item in filelist if re.match(r'(.*)\.txt',item)]

    def check_url(self,url):
        pattern = r'(.*)(很抱歉，您的贴子已被系统删除|很抱歉，该贴已被删除。)(.*)'
        html = self.get_html(url,method=self.method)
        # print(html)
        if re.match(pattern,html):
            # 被删帖了
            return False
        else:
            return True

    def not_my_comment(self,url,filename):
        """
        复制了别人的链接，清理掉
        """
        name = re.split(r'(game)|(phone)',filename)[0]
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        r = requests.get(url,headers=headers)
        ret_list = re.findall('{}'.format(name),r.text)
        if ret_list:
            return False
        else:
            return True
     
    
    def get_html(self,url,method='requests'):
        if method=='requests':
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
            }
            r = requests.get(url,headers=headers)
            r.encoding = 'utf-8'
            html = r.text
        if method=='selenium':
            self.driver.get(url)
            html = self.driver.execute_script("return document.documentElement.outerHTML")
        return html

    def parse_one_file(self,filename):
        """
        清理一个文件的链接
        params:{
            filename[str]:文件名字
        }
        """
        filepath = os.path.join(self.filedir,filename)
        item_list = self.get_url_list(filepath)
        print(filename)
        print('原url数量：{}'.format(len(item_list)))
        save_list = []
        for name,url in tqdm(item_list):
            if self.check_url(url) and not self.not_my_comment(url,filename):
                save_list.append([name,url])
                time.sleep(1)
        print('剩余数量：{}'.format(len(save_list)))
        with open(filepath,'w',encoding='utf-8') as f:
            for item in save_list:
                f.write(item[0]+' '+item[1])

        del_path = os.path.join(self.deldir,filename)
        del_list = self.get_url_list(filename)

        item_set = set([item[0]for item in item_list]) if item_list else {}
        if save_list:
            item_set -= set([item[0]for item in save_list])
        if del_list:
            item_set -= set([item[0]for item in del_list])
        del_save_name_list = list(item_set) if item_set else []
        del_save_list = [item for item in item_list if item[0] in del_save_name_list]

        with open(del_path,'a+',encoding='utf-8') as f:
            for item in del_save_list:
                f.write(item[0]+' '+item[1])
        print('新增被删数量：{}'.format(len(del_save_list)))


    def run(self):
        filelist = self.get_parse_list(self.get_file_list(),self.black_list)
        for filename in filelist:
            self.parse_one_file(filename)   

    def get_parse_list(self,itemlist,blacklist):
        return list(set(itemlist)-set(blacklist))

    def add_black_list(self,black_list):
        self.black_list = black_list

        

if __name__ == "__main__":
    u = UrlFilter(method='requests')
    # print(u.get_file_list())
    # url = 'http://tieba.baidu.com/p/7162909681?share=9105&fr=share&share_from=post&sfc=copy&client_type=2&client_version=12.1.8.1&st=1608621310&unique=D5C01B2387930B32C979D3526C0B58F2'
    # url1 = 'http://tieba.baidu.com/p/7161169091?share=9105&fr=share&share_from=post&sfc=copy&client_type=2&client_version=12.1.8.1&st=1608533252&unique=A12AA1FF0C92BCE2851B14466F5D41A5'
    # r = requests.get(url)
    # print(u.check_url(url))
    black_list = []
    u.add_black_list(black_list)
    u.run()