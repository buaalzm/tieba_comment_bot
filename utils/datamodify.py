import pymysql
import re
import sys
import os
from tqdm import tqdm

sys.path.append(os.path.dirname(__file__))
from mysqlservice import MySQLService


class DataModify(MySQLService):
    def clear_front_rule(self,sentence):
        """
        清除句子里面不适合作为开头的部分
        """
        table = 't_game_sentence'
        try:
            sen_old = sentence
            pattern = r'^(([\s]*[\d]*[\.,，、:：-])[\s\d]*)|^(但[是]?|另外|比如|而且|其次|于是|毕竟|终于|所以|总而言之|其他|还有[的]?|不过|ps:|[最然]后|[第]*[一二三四五])|^[\)），,①②③④⑤⑥◆\|"]'
            s = re.sub(pattern,'',sen_old)
            temp = re.sub(pattern,'',s)
            while s!=temp:
                s = temp
            if sen_old!=s:
                # 有改动，update
                sql = "UPDATE {table} SET sentence='{sen_new}',len={len} WHERE sentence='{sen_old}';".format(table=table,sen_new=s,len=len(s),sen_old=sen_old)
                self.cursor.execute(sql)
                self.connect.commit()
        except:
            print('更新失败')

    def split_line_remove(self,sentence,thre=7):
        """
        清除分割线
        """
        table = 't_game_sentence'       
        resoult={}
        for i in sentence:
            if i not in ',，':
                resoult[i]=sentence.count(i)
        count_list = [val for val in resoult.values()]
        count = 0 if len(count_list)==0 else max(count_list)
        if count>thre:
            # 判定为分割线
            sql = "DELETE FROM {table} WHERE sentence='{sen}'".format(table=table,sen=sentence)
            self.cursor.execute(sql)
            self.connect.commit()
        
    def sentence_process(self):
        """
        清洗爬取的句子，去除分割线，去除不适合开头的词，符合，数字等
        """
        ret = self.select(table='t_game_sentence',field='sentence')
        sen_list = [item['sentence'] for item in ret] # 句子列表
        print('处理前:{}条'.format(len(sen_list)))
        for sen in tqdm(sen_list):
            self.clear_front_rule(sentence=sen)
            self.split_line_remove(sentence=sen,thre=7)
        ret = self.select(table='t_game_sentence',field='sentence')    
        print('处理后:{}条'.format(len(ret)))

    def tag_replace(self,tag_old_list,tag_new_list):
        table = 't_game_tag'
        assert len(tag_old_list)==len(tag_new_list)
        for old,new in zip(tag_old_list,tag_new_list):
            sql = "UPDATE {table} SET tag='{new}' WHERE tag='{old}'".format(table=table,new=new,old=old)
            self.cursor.execute(sql)
            self.connect.commit()


if __name__ == "__main__":
    dm = DataModify()
    dm.sentence_process()
    # dm.update_id(table='t_game_sentence')
    dm.tag_replace(tag_old_list=['优化相关'],tag_new_list=['优化不足'])