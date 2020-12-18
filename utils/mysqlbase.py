import pymysql


class MySQLBase():
    def __init__(self,host='127.0.0.1',user='root',password='210113',charset='utf8',db='yangmao',port=3306,use_unicode=True):
        self.update_db_settings(host=host,user=user,password=password,charset=charset,db=db,port=port,use_unicode=use_unicode)

    def update_db_settings(self,host='127.0.0.1',user='root',password='210113',charset='utf8',db='yangmao',port=3306,use_unicode=True):
        self.connect = pymysql.connect(
            host=host,  # 数据库地址
            port=port,  # 数据库端口
            db=db,  # 数据库名
            user=user,  # 数据库用户名
            passwd=password,  # 数据库密码
            charset=charset,  # 编码方式
            use_unicode=use_unicode)
        self.cursor = self.connect.cursor()