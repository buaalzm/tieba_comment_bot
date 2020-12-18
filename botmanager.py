from tieba_bot import TiebaBot
from utils.gamecommentgenerator import GameCommentGenerator
from utils.phonecommentgenarator import PhoneCommentGenerator

import os
from tqdm import tqdm


class BotManager():
    def __init__(self,username,device,item_type):
        self.username = username
        self.device = device if device else None
        self.item_type = item_type
        save_name = username + item_type + '.txt'
        log_name = username + item_type + '.log'
        self.save_path = os.path.join('out',save_name)
        self.log_path = os.path.join('log',log_name)
        self.bot = TiebaBot(device=self.device,save_file_name=save_name,log_file_name=log_name,item_type=item_type,username=username)

        assert item_type in ['phone','game']
        if item_type == 'phone':
            self.generator = PhoneCommentGenerator()
            self.item_list = self.generator.get_avail_phone_name()
        if item_type == 'game':
            self.generator = GameCommentGenerator()
            self.item_list = self.generator.get_name_list()

        done_list = self.get_done_list(self.save_path)
        self.item_list = list(set(self.item_list)-set(done_list))
    
    def get_done_list(self,filename):
        """
        提取出已经弄完的项
        目录不存在返回空列表
        """
        ret = []
        if not os.path.exists(filename):
            return []
        with open(filename,'r') as f:
            for line in f:
                ret.append(line.split(' ')[0])
        return ret

    def get_item_list_from_file(self,filepath):
        """
        从已经输出好的文件中，提取出可以用的item
        """
        return self.get_done_list(filepath)

    def run(self):
        for item in tqdm(self.item_list):
            comment = self.generator.gen_one_comment(item)
            star = self.generator.get_star(item)
            print('\nname: {}\ncomment:{}\nstar:{}'.format(item,comment,star))
            if not comment:
                continue
            try:
                self.bot.action(subject=item,comment=comment,star=star)
            except:
                self.bot.prepare_next()

