from tieba_bot import TiebaBot
from utils.gamecommentgenerator import GameCommentGenerator
from utils.phonecommentgenarator import PhoneCommentGenerator

import os
from tqdm import tqdm
from random import sample,randint
import time
import re


class BotManager():
    def __init__(self,username,device,item_type):
        self.username = username
        self.device = device if device else None
        self.item_type = item_type
        save_name = username + item_type + '.txt'
        log_name = username + item_type + '.log'
        self.save_name = save_name
        self.save_path = os.path.join('out',save_name)
        self.log_path = os.path.join('log',log_name)
        self.bot = TiebaBot(device=self.device,save_file_name=save_name,log_file_name=log_name,item_type=item_type,username=username)
        self.count = 0

        assert item_type in ['phone','game']
        if item_type == 'phone':
            self.generator = PhoneCommentGenerator()
            self.item_list = self.generator.get_avail_phone_name()
        if item_type == 'game':
            self.generator = GameCommentGenerator()
            self.item_list = self.generator.get_name_list()

        done_list = self.get_done_list(self.save_path)
        submit_list = self.get_submit_list(self.save_name)
        self.item_list = list(set(self.item_list)-set(done_list)-set(submit_list))
    
    def get_done_list(self,filename):
        """
        提取出已经弄完的项
        目录不存在返回空列表
        """
        ret = []
        if not os.path.exists(filename):
            return []
        with open(filename,'r',encoding='utf-8') as f:
            for line in f:
                ret.append(line.split(' ')[0])
        return ret

    def get_submit_list(self,filename):
        """
        提取出已经提交过的项
        """ 
        item_list = []
        submit_dir = os.path.join(os.path.dirname(__file__),'submit')
        pattern = r'^((?!\.).)*$' #　不含．表示文件夹
        dir_list = os.listdir(submit_dir)
        file_path_list = [os.path.join(submit_dir,item,filename) for item in dir_list if re.match(pattern,item)]
        for file_path in file_path_list:
            if os.path.exists(file_path):
                with open(file_path,'r',encoding='utf-8') as f:
                    for line in f:
                        item_list.append(line.split(' ')[0])
        return item_list

    def get_item_list_from_file(self,filepath):
        """
        从已经输出好的文件中，提取出可以用的item
        """
        return self.get_done_list(filepath)

    def run(self,out_num=15):
        for item in tqdm(self.item_list):
            comment = self.generator.gen_one_comment(item)
            star = self.generator.get_star(item)
            print('\nname: {}\ncomment:{}\nstar:{}'.format(item,comment,star))
            if not comment:
                continue
            try:
                self.run_until_put_one(subject=item,comment=comment,star=star)
            except:
                self.bot.prepare_next()
            if self.count >= out_num:
                return
            # time.sleep(randint(40,80))

    def run_until_put_one(self,subject,comment,star):
        ret = self.bot.action(subject=subject,comment=comment,star=star)
        while not ret:
            item = sample(self.item_list,1)[0]
            comment = self.generator.gen_one_comment(item)
            star = self.generator.get_star(item)
            print('\nname: {}\ncomment:{}\nstar:{}'.format(item,comment,star))
            self.item_list.remove(item)
            ret = self.bot.action(subject=item,comment=comment,star=star)
        self.count+=1

    def run_one(self):
        if not self.item_list:
            print('item list vacant')
            return
        item = sample(self.item_list,1)[0]
        comment = self.generator.gen_one_comment(item)
        star = self.generator.get_star(item)
        print('\nname: {}\ncomment:{}\nstar:{}'.format(item,comment,star))
        self.item_list.remove(item)
        if not comment:
            return
        try:
            self.run_until_put_one(subject=item,comment=comment,star=star)
            self.count+=1
        except:
            self.bot.prepare_next()


if __name__ == "__main__":
    bm = BotManager(username='L7t8p14DKpb',device='127.0.0.1:62033',item_type='game')
    print(bm.get_submit_list(bm.save_name))

