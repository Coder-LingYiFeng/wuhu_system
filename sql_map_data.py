# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年04月19日
"""
import pymysql
import requests
import json
from settings import *


def init_map_data():
    conn = pymysql.connect(  # 与mysql建立连接
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')
    cursor = conn.cursor()  # 获取游标

    sql = 'drop table map_date;'
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交事务
        print('map_data数据表初始化成功！！！')
    except Exception as e:
        print('表不存在，初始化失败！！！\n失败原因：')
        print(e)
        conn.rollback()  # 回滚撤销
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接


def create():
    init_map_data()
    conn = pymysql.connect(  # 与mysql建立连接
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8')
    cursor = conn.cursor()  # 获取游标

    sql = 'create table map_date(' \
          'id int unsigned not null primary key auto_increment,' \
          'name varchar(20),' \
          'value varchar(15));'
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交事务
        print('map_data数据表创建成功！！！')
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
    sql = 'insert map_date(name, value) values(%s, %s)'
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
        print('写入sql成功！')


def get_map_data():
    url = 'http://www.wuhu.gov.cn/site/label/8888?isJson=true&labelName=oneToFiveMessagePm&IsAjax=1&dataType=JSON'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
        "Referer": "http://www.wuhu.gov.cn/",
        "Host": "www.wuhu.gov.cn",
        "Upgrade-Insecure-Requests": "1"
    }
    resp = requests.get(url, headers=headers)
    data = json.loads(resp.text)
    XQTop10 = data["obj"][1]["XQTop10"]
    xq_top_ = XQTop10["原三山区"]
    del XQTop10["原三山区"]
    XQTop10["弋江区"] = str(int(XQTop10["弋江区"]) + int(xq_top_))
    for key in XQTop10.keys():
        sqlwrite([key, XQTop10[key]])
    # print(XQTop10)


def sql_map_data_run():
    create()
    get_map_data()
