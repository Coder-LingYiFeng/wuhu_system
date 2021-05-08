# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年01月28日
"""
import requests
import json
import time
import re
from sql_bottom_car import *


def modular_four():
    def bottom_car(ye):
        url = f'http://www.wuhu.gov.cn/OneToFiveMessageBoard//getSzxxMessageBoardPageLst?&siteId=6787231&pageS' \
              f'ize=15&pageIndex={ye}&isJson=true&ids=6787581%2C6787571&action=singleList&isPageMore=true&labelNam' \
              f'e=messageBoardPageList'
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (K'
                              'HTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                'Referer': 'http://www.wuhu.gov.cn/zmhd/12345zfztc/index.html',
                'Cookie': 'UM_distinctid=1774ce92b395a6-07b723d6cfdb36-13e3563-144000-1774ce92b3aa03; CNZZDATA127964726'
                          '9=1693332468-1611902883-https%253A%252F%252Fwww.baidu.com%252F%7C1611902883; SHIROJSESSIO'
                          'NID=13187a35-8731-4df9-8d53-6fc8dd0d65cd',
                'X-Requested-With': 'XMLHttpRequest',
                'Host': 'www.wuhu.gov.cn'
            }
        res = requests.get(url, headers=headers, timeout=10).content
        data_dict = json.loads(res)
        # print(data_dict)
        data_list = data_dict['page']['data']
        # print(data_list)
        for line in range(15):  # 循环每一条信息
            sqlstr = []
            try:
                sqlstr.append(data_list[line]['addDate'].replace('-', '.') + ' ')
                # print(sqlstr)
            except KeyError:
                sqlstr.append('NULL')
            # sqlstr.append(data_list[line]['addDate'][:7].replace('-', '.')+' ')  # 读取信息中的时间，切取年月信息
            message = data_list[line]['messageBoardContent']  # 读取内容追加到列表
            res = re.findall(r'[\u4e00-\u9fa5]', message)  # 匹配中文
            message = ''.join(res)
            sqlstr.append(message)
            sqlstr.append(data_list[line]['className'])
            sqlstr.append(data_list[line]["receiveUnitName"])
            try:
                sqlstr.append(data_list[line]['resources'])
                # print(sqlstr)
            except KeyError:
                try:
                    sqlstr.append(data_list[line]['resourcesType'])
                    # print(sqlstr)
                except KeyError:
                    sqlstr.append('NULL')
            # print(sqlstr)

            try:
                sqlstr.append(data_list[line]['replyDate'].replace('-', '.') + ' ')
            except KeyError:
                sqlstr.append('NULL')

            sqlstr.append(data_list[line]['link'])
            sqlstr.append(data_list[line]['title'])
            print(sqlstr)
            sqlwrite(sqlstr)
        time.sleep(0.5)


    # 此次工作的开始
    create_bottom_car()

    for page in range(1, 158):
        try:
            bottom_car(page)
            print(f'第{page}页读取完毕')
        except Exception:
            print('已到达最后一条数据！')
