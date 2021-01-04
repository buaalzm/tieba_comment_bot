import pymysql

# 建库和建表
con = pymysql.connect(host='localhost', user='root',
                      passwd='210113', charset='utf8')
cur = con.cursor()
# 开始建库
# cur.execute("create database yangmao character set utf8;")
# 使用库
cur.execute("use yangmao;")
# 建表
try:
    cur.execute("create table t_phone_comment_url(\
        id int PRIMARY KEY AUTO_INCREMENT,\
        name varchar(256),\
        url varchar(256)\
        ) character set utf8;")
except:
    print('table exists')
try:
    cur.execute("create table t_phone_comment(\
        id int PRIMARY KEY AUTO_INCREMENT,\
        `name` varchar(256),\
        `like` varchar(256),\
        dislike varchar(256),\
        appearance varchar(256),\
        performance varchar(256),\
        fluency varchar(256),\
        camera varchar(256),\
        other varchar(256)\
        )character set utf8;")
except:
    print('table exists')
try:  
    cur.execute("create table t_phone_score(\
        id int PRIMARY KEY AUTO_INCREMENT,\
        name varchar(256),\
        score varchar(256),\
        cheap varchar(256),\
        display varchar(256),\
        fluency varchar(256),\
        battery varchar(256),\
        camera varchar(256)\
        )character set utf8;")
except:
    print('table exists')
try:
    cur.execute("create table t_game_comment_url(\
        id int PRIMARY KEY AUTO_INCREMENT,\
        name varchar(256),\
        url varchar(256)\
        ) character set utf8;")
except:
    print('table exists')
try:
    cur.execute("create table t_game_sentence(\
        id int PRIMARY KEY AUTO_INCREMENT,\
        name varchar(256),\
        sentence varchar(256),\
        len int\
        ) character set utf8;")
except:
    print('table exists')
try:
    cur.execute("create table t_game_tag(\
        id int PRIMARY KEY AUTO_INCREMENT,\
        name varchar(256),\
        tag varchar(256),\
        attitude varchar(256)\
        ) character set utf8;")
except:
    print('table exists')
try:
    cur.execute("create table t_game_score(\
        id int PRIMARY KEY AUTO_INCREMENT,\
        name varchar(256),\
        score varchar(256)\
        ) character set utf8;")
except:
    print('table exists')