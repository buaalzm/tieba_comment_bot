"""
从数据库读取句子片段，评分，tag等信息，生成评论
"""
import os
import sys
sys.path.append(os.path.dirname(__file__))

from mysqlservice import MySQLService
from random import sample,shuffle,seed,randint


class GameCommentGenerator():
    def __init__(self):
        self.db = MySQLService()

    def get_name_list(self):
        sql = "select DISTINCT name from t_game_sentence"
        self.db.cursor.execute(sql)
        ret = self.db.cursor.fetchall()
        namelist = [item[0] for item in ret]
        return namelist

    def gen_one_comment(self,name):
        """
        根据名字，生成一条评论，名字必须是在namelist中的
        """
        comment_list = self.db.filter(table='t_game_sentence',field=['name','sentence','len'],name=name)
        posi_list,neg_list = self.get_tag_list(name)
        # print(len(comment_list),posi_list,neg_list,star)

        if(len(comment_list)<5):
            return ''

        # 定义生成的规则

        start_comment = name + '这'+ GameCommentGenerator.sample_one(['款','个',''])+'游戏，'
        play_time_str = '{}个月'.format(GameCommentGenerator.sample_one(['一','两','三','四','五','六','1','2','3','4','5','6','7']))
        play_str = '我玩了'+GameCommentGenerator.sample_one(['大概','有','大概有',''])+ \
            GameCommentGenerator.sample_one([play_time_str,'半年','一年'])+ \
            GameCommentGenerator.sample_one(['多',''])+'了。'

        start_comment = start_comment + GameCommentGenerator.sample_one([play_str,'']) # 起始句

        comment_choice_list = []
        sen_len = 0
        while sen_len<120 and comment_list:
            sen = GameCommentGenerator.sample_one(comment_list)
            sen_len=sen_len+sen['len']
            comment_choice_list.append(sen['sentence'])
            comment_list.remove(sen)
        
        sentence_comment = '' # 用句子拼接出的中段
        for sen in comment_choice_list:
            sentence_comment += sen + '。'

        summary_comment = '' # 总结句
        if posi_list or neg_list:
            summary_start_choice = ['总而言之','简而言之','概括一下','总结一下','反正','如果总结一下的话']
            summary_comment+=sample(summary_start_choice,1)[0]
            summary_comment+=sample(['，这是一款','，这是一个'],1)[0]
            for item in sample(posi_list,min(randint(2,5),len(posi_list))):
                summary_comment+=item+','
            summary_comment = summary_comment[:-1]+'的游戏。' # 去掉逗号
            if neg_list:
                summary_comment+=sample(['就是有点','美中不足的是','就是','缺点是'],1)[0]
            for item in neg_list:
                summary_comment+=item+','
            summary_comment = summary_comment[:-1] + '。'
        
        comment = start_comment + sentence_comment + summary_comment
        
        return comment
        

    def get_score(self, name):
        ret = self.db.filter(table='t_game_score',field='score',name=name)
        if not ret:
            return 3
        score = float(ret[0]['score'])
        if score<0.1:
            score = 4
        return score/2

    def get_star(self,name):
        return round(self.get_score(name))

    def get_tag_list(self,name):
        """
        根据正面负面拆分开
        """
        tag_list = self.db.filter(table='t_game_tag',field=['name','tag','attitude'],name=name)
        posi_list = [item['tag'] for item in tag_list if item['attitude']=='posi']
        neg_list = [item['tag'] for item in tag_list if item['attitude']=='neg']
        return posi_list,neg_list

    @staticmethod
    def sample_one(choice_list):
        return sample(choice_list,1)[0]


if __name__ == "__main__":
    g = GameCommentGenerator()
    print(g.gen_one_comment('猎魂觉醒'))
