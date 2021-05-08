# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年01月28日
"""
import pymysql
from settings import *


def init_bottom_car():
    conn = pymysql.connect(  # 与mysql建立连接
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')
    cursor = conn.cursor()  # 获取游标

    sql = 'drop table bottom_car;'
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交事务
        print('bottom_car数据表初始化成功！！！')
    except Exception as e:
        print('初始化失败！！！\n表不存在！')
        print(e)
        conn.rollback()  # 回滚撤销
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接


def create_bottom_car():
    init_bottom_car()
    conn = pymysql.connect(  # 与mysql建立连接
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')
    cursor = conn.cursor()  # 获取游标

    sql = 'create table bottom_car(' \
          'id int unsigned not null primary key auto_increment,' \
          'year_day varchar(20),' \
          'message varchar(5000),' \
          'problem_type varchar(10),' \
          'receiveunitname varchar(50),' \
          'method varchar(20), replyDate varchar(20), link varchar(150), title varchar(500));'
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交事务
        print('bottom_car数据表创建成功！！！')
    except Exception as e:
        print('创建失败！！！\n失败原因：')
        print(e)
        conn.rollback()  # 回滚撤销
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接


def sqlwrite(sql_str_list):  # 写入数据
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')

    cursor = conn.cursor()
    sql = 'insert bottom_car(year_day, message, problem_type, receiveunitname, method, replyDate, link, title) values(%s, %s, %s, %s, %s, %s, %s,%s)'
    try:
        cursor.execute(sql, sql_str_list)
        conn.commit()
    except Exception as e:
        print('写入出错！！！\n出错原因：')
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
