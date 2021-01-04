"""
生成数码评论
"""
import os
import sys
sys.path.append(os.path.dirname(__file__))

from mysqlservice import MySQLService
from random import sample,shuffle,seed,randint


class PhoneCommentGenerator():
    def __init__(self):
        self.db = MySQLService()

    def get_avail_phone_name(self):
        name = self.db.select(table='t_phone_comment',field='name')
        comment_avail_name = [item['name'] for item in name]
        name = self.db.select(table='t_phone_score',field='name')
        score_avail_name = [item['name'] for item in name]
        avail_name = list(set(comment_avail_name)&set(score_avail_name))
        return avail_name

    def gen_one_comment(self,name):
        comment = self.db.filter(table='t_phone_comment',field=['name','like','dislike','appearance','performance','fluency','camera','other'],
        name=name)
        # print(comment)
        like_list = [item['like'] for item in comment if item['like']]
        dislike_list = [item['dislike'] for item in comment if item['dislike']]
        appearance_list = [item['appearance'] for item in comment if item['appearance']]
        performance_list = [item['performance'] for item in comment if item['performance']]
        fluency_list = [item['fluency'] for item in comment if item['fluency']]
        camera_list = [item['camera'] for item in comment if item['camera']]
        other_list = [item['other'] for item in comment if item['other']]
        # print(len(like_list),len(dislike_list),len(appearance_list),len(performance_list),len(fluency_list),len(camera_list),len(other_list))

        pc_list = ['戴尔g3']
        pad_list = ['ipad2018','ipadmini2','ipadmini3','小米平板']

        if name in pc_list:
            comment = name + '这款电脑，'
        if name in pad_list:
            comment = name + '这款平板，'
        else:
            comment = name + '这款手机，'
            
        if like_list:
            comment = comment + PhoneCommentGenerator.sample_one(['总体来说','给我的总体印象是']) + PhoneCommentGenerator.sample_one(like_list)+'。'
        if dislike_list:
            comment = comment + PhoneCommentGenerator.sample_one(['美中不足的是','缺点是'])+ PhoneCommentGenerator.sample_one(dislike_list)
        
        comment = comment + '\n'

        comment_list = []
        if appearance_list:
            comment_list.append('外观上，'+PhoneCommentGenerator.sample_one(appearance_list))
        if performance_list:
            comment_list.append('性能上，'+PhoneCommentGenerator.sample_one(performance_list))
        if fluency_list:
            comment_list.append('流畅度上，'+PhoneCommentGenerator.sample_one(fluency_list))
        if camera_list:
            comment_list.append('拍照方面，'+PhoneCommentGenerator.sample_one(camera_list))

        # shuffle(comment_list)
        comment_list = sample(comment_list,randint(min(2,len(comment_list)),len(comment_list)))
        comment = comment + ''.join(comment_list) + '\n'
        if other_list and len(comment)<500:
            comment = comment + PhoneCommentGenerator.sample_one(other_list)

        return comment if len(comment)<500 else comment[:499]
        
    @staticmethod
    def sample_one(choice_list):
        return sample(choice_list,1)[0]

    def get_score(self, name):
        ret = self.db.filter(table='t_phone_score',field='score',name=name)
        score = float(ret[0]['score'])
        if score<0.1:
            score = 4
        return score

    def get_star(self,name):
        return round(self.get_score(name))
    

if __name__ == "__main__":
    c = PhoneCommentGenerator()
    seed()
    print(c.gen_one_comment(name='小米8'))
    # print(c.get_star('荣耀9'))