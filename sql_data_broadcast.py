# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年01月28日
"""
import pymysql
from settings import *


def init_data_broadcast():
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')

    cursor = conn.cursor()
    sql = 'drop table data_broadcast'
    try:
        cursor.execute(sql)
        conn.commit()
        print('data_broadcast数据表初始化成功!')
    except Exception as e:
        print('初始化失败！表不存在！')
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def creat_data_broadcast():
    init_data_broadcast()
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')

    cursor = conn.cursor()
    sql = 'create table data_broadcast(' \
          'id int unsigned not null primary key auto_increment,' \
          'type varchar(10),' \
          'day_accept int,' \
          'day_end int,' \
          'month_accept int,' \
          'month_end int,' \
          'year_accept int,' \
          'year_end int,' \
          'all_accept int,' \
          'all_end int);'
    try:
        cursor.execute(sql)
        conn.commit()
        print('data_broadcast数据表创建成功!')
    except Exception as e:
        print('创建出错！表已存在！')
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def sql_write(sql_str_list):  # 写入数据
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')

    cursor = conn.cursor()
    sql = 'insert data_broadcast(type, day_accept, day_end, month_accept, month_end, year_accept, year_end, ' \
          'all_accept, all_end) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
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


def sql_read(n):  # 写入数据
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')

    cursor = conn.cursor()
    sql = f'select type, day_accept, day_end, month_accept, month_end, year_accept, year_end, all_accept, all_end ' \
          f'from data_broadcast where id = {n}'
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        conn.commit()
        return list(row)
    except Exception as e:
        print('查询出错！！！\n出错原因：')
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
