import pymysql.cursors
from items import PhoneCommentUrlItem,PhoneCommentItem,PhoneScoreItem


class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='yangmao',  # 数据库名
            user='root',  # 数据库用户名
            passwd='210113',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if isinstance(item,PhoneCommentUrlItem):
            self.save_url(item)
        if isinstance(item,PhoneCommentItem):
            self.save_comment(item)
        if isinstance(item,PhoneScoreItem):
            self.save_score(item)

    def save_url(self,item):
        self.cursor.execute(
            """insert into t_phone_comment_url(name, url)
            value (%s, %s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['name'],  # item里面定义的字段和表字段对应
             item['url'],))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def save_comment(self,item):
        self.cursor.execute(
            "insert into t_phone_comment(`name`,`like`,dislike,appearance,performance,fluency,camera,other) value (%s,%s,%s,%s,%s,%s,%s,%s)",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['name'],  # item里面定义的字段和表字段对应
             item['like'],
             item['dislike'],
             item['appearance'],
             item['performance'],
             item['fluency'],
             item['camera'],
             item['other'],))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def save_score(self,item):
        self.cursor.execute(
            """insert into t_phone_score(name,score,cheap,display,fluency,battery,camera)
            value (%s, %s,%s, %s,%s, %s,%s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['name'],  # item里面定义的字段和表字段对应
             item['score'],
             item['cheap'],
             item['display'],
             item['fluency'],
             item['battery'],
             item['camera'],))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回
