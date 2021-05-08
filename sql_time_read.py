# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年01月28日
"""
import pymysql


def sql_read(sql_str):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        database='wuhu',
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = sql_str
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        conn.commit()
        return list(row)[0]
    except Exception as e:
        print('查询出错！')
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_id_max():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        database='wuhu',
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = 'select max(id) from shizhang'
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        conn.commit()
        return list(row)[0]+1  # 后续的ruage参数，提前加一
    except Exception as e:
        print('查询出错！')
        print(e)
    finally:
        cursor.close()
        conn.close()