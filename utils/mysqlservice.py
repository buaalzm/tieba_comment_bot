import pymysql
import sys
import os
sys.path.append(os.path.dirname(__file__))
from mysqlbase import MySQLBase
from tqdm import tqdm


class MySQLService(MySQLBase):
    def __init__(self,host='127.0.0.1',user='root',password='210113',charset='utf8',db='yangmao',port=3306,use_unicode=True):
        super().__init__(host=host,user=user,password=password,charset=charset,db=db,port=port,use_unicode=use_unicode)
    
    def check_exists(self,table,field,value):
        # sql = "select count(1) as cnt from {table} where ".format(table=table)
        # for key in kwargs:
        #     sql = sql + key+'='+"'"+kwargs[key]+"'"+' and '
        # sql = sql[:-4]
        sql = "select count(1) as cnt from {table} where '{field}' = '{value}'".format(table=table,field=field,value=value)
        # print(sql)
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        if ret[0][0] != 0:
            return True
        else:
            return False

    def select(self,table,field):
        if not field:
            return []
        if isinstance(field,str):
            field_str = field
            field = [field]
        if isinstance(field,list):
            field_str = ''
            for item in field:
                field_str = field_str+'`'+item+'`,'
            field_str = field_str[:-1]
        sql = "select {field_str} from {table};".format(field_str=field_str,table=table)
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        # print(ret)
        result = []
        for onequery in ret:
            d = {}
            for i,f in enumerate(field):
                d[f]=onequery[i]
            result.append(d)
        return result

    def update_id(self,table):
        sql = "select id from {table}".format(table=table)
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        for i,item in tqdm(enumerate(ret)):
            sql = "UPDATE {table} SET id={id_new} WHERE id={id_old};".format(table=table,id_new=i+1,id_old=item[0])
            self.cursor.execute(sql)
            self.connect.commit()

    def filter(self,table,field,**kwargs):
        """
        table[str]:
        field[list[str]]:选取的字段
        kwargs:筛选条件
        """
        if not field:
            return []
        if isinstance(field,str):
            field_str = field
            field = [field]
        if isinstance(field,list):
            field_str = ''
            for item in field:
                field_str = field_str+'`'+item+'`,'
            field_str = field_str[:-1]
        sql = "select {field_str} from {table} ".format(field_str=field_str,table=table)
        sql = sql + 'where '
        for key in kwargs:
            sql = sql + key+'='+"'"+kwargs[key]+"'"+' and '
        # print(sql)
        sql = sql[:-4]
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        # print(ret)
        result = []
        for onequery in ret:
            d = {}
            for i,f in enumerate(field):
                d[f]=onequery[i]
            result.append(d)
        return result

    def insert(self,table,**kwargs):
        field_str = ''
        value_str = ''
        for key in kwargs:
            field_str = field_str+'`'+key+'`,'
            if isinstance(kwargs[key],str):
                value_str = value_str+"'"+kwargs[key]+"',"
            else:
                value_str = value_str+str(kwargs[key])+','
        field_str = field_str[:-1]
        value_str = value_str[:-1]
        sql = "INSERT INTO {table} ({fields}) VALUES ({values});".format(table=table,fields=field_str,values=value_str)
        self.cursor.execute(sql)
        self.connect.commit()

    def raw(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()




if __name__ == "__main__":
    ce = MySQLService()
    # ce.check_exists(table='t_phone_comment_url',field='name',value='iphone8')
    # ce.check_exists(table='t_phone_comment_url',field='name',value='苹果x')
    # print(ce.select(table='t_phone_comment_url',field='name'))
    # print(ce.select(table='t_phone_comment_url',field=['id','name']))
    ce.update_id('t_game_sentence')
    ce.update_id('t_game_comment_url')
    ce.update_id('t_game_score')
    ce.update_id('t_game_tag')