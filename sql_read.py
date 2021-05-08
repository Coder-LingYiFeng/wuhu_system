# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年01月28日
"""
import pymysql
from settings import *


def sqlread(sql_str):
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database='wuhu',
        charset='utf8'
    )

    cursor = conn.cursor()
    sql = sql_str
    try:
        cursor.execute(sql)
        row = cursor.fetchall()
        for line in row:
            url1 = line[1]
            # print(url1)
            jsonstr1 = line[2]
            # print(jsonstr1)
            id1 = line[3]
            # print(id1)
            name1 = line[4]
            # print(name1)
            danwei = line[5]
            # print(danwei)
            return url1, jsonstr1, id1, name1, danwei
    except Exception as e:
        print('读取出错！')
        print(e)
    finally:
        cursor.close()
        conn.close()