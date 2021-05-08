# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年01月28日
"""
import pymysql
import csv
from settings import *


def create_input_data():
    conn = pymysql.connect(  # 与mysql建立连接
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')
    cursor = conn.cursor()  # 获取游标

    sql = 'create table input_data(' \
          'id tinyint unsigned not null primary key auto_increment,' \
          'url varchar(300),' \
          'jsonstr varchar(500),' \
          'id_data varchar(30),' \
          'name varchar(20),' \
          'danwei varchar(20));'
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交事务
        print('input_data数据表创建成功！！！')
    except Exception as e:
        print('创建失败！！！\n失败原因：')
        print(e)
        conn.rollback()  # 回滚撤销
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接


def sql_write(sql_str_list):  # 写入数据
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')

    cursor = conn.cursor()
    sql = 'insert input_data(url, jsonstr, id_data, name, danwei) values(%s, %s, %s, %s, %s)'
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


def create_wuhu():
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='sys',
        charset='utf8')

    cursor = conn.cursor()
    sql = 'create database wuhu;'
    try:
        cursor.execute(sql)
        conn.commit()
        print('wuhu数据库创建成功！！！')
    except Exception as e:
        print('创建出错！！！\n出错原因：')
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def ready():
    create_wuhu()  # 创建wuhu
