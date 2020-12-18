import sys
import os
sys.path.append(os.path.dirname(__file__))
from mysqlservice import MySQLService


class GameDBService(MySQLService):
    def url_insert(self,name,url):
        """
        在表中添加评论的url
        """
        table = 't_game_comment_url'
        if not self.check_exists(table=table,name=name):
            self.insert(table=table,name=name,url=url)
        else:
            print('元素重复：name={},url={}'.format(name,url))

    def sentence_insert(self,name,sentence):
        """
        将句子碎片添加入库
        """
        table = 't_game_sentence'
        if not self.check_exists(table=table,sentence=sentence) and len(sentence)<255:
            self.insert(table=table,name=name,sentence=sentence,len=len(sentence))
        else:
            print('元素重复：name={},sentence={}'.format(name,sentence[:20]))

    def tag_insert(self,name,tag,attitude):
        """
        标签入库
        """
        table = 't_game_tag'
        assert attitude in ['posi','neg']
        if not self.check_exists(table=table,name=name,tag=tag):
            self.insert(table=table,name=name,tag=tag,attitude=attitude)
        else:
            print('元素重复：name={},tag={},attitude={}'.format(name,tag,attitude))

    def score_insert(self,name,score):
        """
        评分入库
        params:
        {
            namep[str]
            score[str]
        }
        """
        table = 't_game_score'
        if not self.check_exists(table=table,name=name):
            self.insert(table=table,name=name,score=score)
        else:
            print('元素重复：name={},score={}'.format(name,score))