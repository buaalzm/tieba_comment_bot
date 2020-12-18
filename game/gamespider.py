from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import sample,randint,seed

from queue import Queue
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime 
import json

import re
import os
import sys
from ipdb import set_trace

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from utils.gamedb import GameDBService


class GameCommentFactory():
    """
    从taptap获取评论
    """
    def __init__(self):
        option = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2,'permissions.default.stylesheet':2}
        option.add_experimental_option("prefs", prefs)
        option.add_argument('headless') # 设置option
        self.driver = webdriver.Chrome(options=option)
        self.db = GameDBService()
        self.subject = ''

    def __del__(self):
        self.driver.quit()
        

    def get_comment_page(self, subject):
        """
        获取评论页面
        """
        self.subject = subject
        # taptap搜索游戏
        self.driver.get('https://www.taptap.com/search/{}'.format(subject))
        # 解析出评论的链接
        comment_css_str = '#js-nav-sidebar-main > div > div > div > div.search-page.search-web-content > div > div.van-tabs__content > div:nth-child(1) > div > div > div:nth-child(1) > div > div:nth-child(2) > div.game-search-item__labels.van-hairline--bottom > div:nth-child(1) > a'
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#js-nav-sidebar-main > div > div > div > div.search-page.search-web-content > div > div.van-tabs__content > div:nth-child(1)')))
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, comment_css_str)))
        except:
            print('{}评论链接未加载出来，可能是没有搜到游戏'.format(subject))
            return False
        comment_button = self.driver.find_element_by_css_selector(comment_css_str)
        comment_url = comment_button.get_attribute('href')
        self.db.url_insert(name=subject,url=comment_url)
        self.driver.get(comment_url) # 转到评论页面
        return True
    
    def get_comment_tag(self):
        """
        官方总结出来的评价tag
        运行这段时应该已经在评价的页面了
        """
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#review-label-list')))
        except:
            print('评论页面未加载出来')
            return [],[]
        score = self.driver.find_element_by_css_selector('#js-nav-sidebar-main > div.container.app-main-container > div > div > section.app-show-main.taptap-page-main > div.show-main-header > div.main-header-text > div.base-info-wrap > span > span > span').text
        self.db.score_insert(name=self.subject,score=score)

        tag_box = self.driver.find_element_by_css_selector('#review-label-list')
        tag_item_list = tag_box.find_elements_by_tag_name('li>div')
        posi_list = []
        neg_list = []
        for item in tag_item_list:
            if 'positive' in item.get_attribute('class') and len(item.text)>1:
                tag = re.sub(r"[A-Za-z0-9\!\%\[\]\,\。\+\.]", "", item.text)
                posi_list.append(tag)
                self.db.tag_insert(name=self.subject,tag=tag,attitude='posi')
            if 'negative' in item.get_attribute('class') and len(item.text)>1:
                tag = re.sub(r"[A-Za-z0-9\!\%\[\]\,\。\+\.]", "", item.text)
                neg_list.append(tag)
                self.db.tag_insert(name=self.subject,tag=tag,attitude='neg')
        
        return posi_list,neg_list

    def get_comment_sentences(self):
        """
        抓取评论
        返回切成小句子的，每个句子结尾不带标点
        return[list]
        """
        body = self.driver.find_elements_by_class_name('item-text-body')
        body = self.driver.find_elements_by_css_selector('div.review-item-text>div.item-text-body')
        lis = [item.text for item in body]
        comment_piece = [] #切成一句一句的
        for item in lis:
            sentences = re.split('。|！|？|\n',str(item))
            sentences = [item for item in sentences if len(item)>=10] # 保留长度大于10的句子
            sentences = [item if item[-1] != '，' else item[:-1] for item in sentences] # 去除逗号
            comment_piece += sentences
        for item in comment_piece:
            try:
                self.db.sentence_insert(name=self.subject,sentence=item)
            except:
                continue
        return comment_piece
    
    def make_comment(self):
        seed()
        posi_list,neg_list = self.get_comment_tag()
        # print(posi_list,neg_list)
        sentences = self.get_comment_sentences()
        # print(sentences)

        lenth = 0 # 字数统计

        sample_comment = '' # 用句子拼出来的评论
        sample_num = min(20,len(sentences))
        first_sample = sample(sentences,sample_num)
        for i in range(sample_num):
            # 字数小于120一直增加句子数量
            sample_comment += first_sample[i]+'。'
            lenth = len(sample_comment)
            if lenth > 120:
                break

        posi_num = len(posi_list) # 抽取的正面评价个数，大于5的随机树
        neg_num = len(neg_list) 
        if len(posi_list)>5:
            posi_num  = randint(3,5)
        if len(neg_list)>5:
            neg_num  = randint(3,5)
        posi_list = sample(posi_list,posi_num)
        neg_list = sample(neg_list,neg_num)

        if len(posi_list)+len(neg_list)==0:
            return sample_comment

        summary_comment = '' # 用tag拼出来的评论
        summary_start_choice = ['总而言之','简而言之','概括一下','总结一下','反正','如果总结一下的话']
        summary_comment+=sample(summary_start_choice,1)[0]
        summary_comment+=sample(['，这是一款','，这是一个'],1)[0]
        for item in posi_list:
            summary_comment+=item+','
        summary_comment = summary_comment[:-1]+'的游戏。' # 去掉逗号
        if not neg_list:
            summary_comment+=sample(['就是有点','美中不足的是','就是','缺点是'],1)[0]
        for item in neg_list:
            summary_comment+=item+','
        summary_comment = summary_comment[:-1] + '。'
        return sample_comment+summary_comment

    def get_comment(self,subject):
        if not self.get_comment_page(subject):
            return ''
        comment = self.make_comment()
        return comment


class MultiGMF():
    def __init__(self,num):
        self.num = num
        self.fqueue = Queue(num)
        self.data = {'games':[]}
        self.count = 0
        for i in range(num):
            self.fqueue.put(GameCommentFactory())
        self.pool = ThreadPool()

    def start(self,items):
        self.total = len(items)
        self.pool.map(self.process_item, items)
        self.pool.close()
        self.pool.join()   

    def process_item(self,name):
        cf = self.fqueue.get()
        self.count = self.count+1
        comment = cf.get_comment(name)
        self.data['games'].append({'name':name,'comment':comment})
        self.fqueue.put(cf)
        print('finish {count} in {total}'.format(count=self.count,total=self.total))

    def save(self):
        with open('out/games{}.json'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")), 'w',encoding='utf-8') as json_file:
            json.dump(self.data,json_file,ensure_ascii=False)

if __name__ == "__main__":
    from utils.fileloader import FileLoader
    from ipdb import set_trace
    fl = FileLoader()
    fl.loadfile('game.txt')
    namelist = fl.get_name_list()
    m = MultiGMF(num=4)
    m.start(namelist)
    m.save()

    