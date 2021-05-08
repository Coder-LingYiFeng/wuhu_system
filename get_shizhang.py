# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年04月01日
"""
import requests
import json
import time
from sql_shizhangxinxiang import *
import re


def modular_two():
    def shizhang_data(ye):
        url = 'http://www.wuhu.gov.cn/OneToFiveMessageBoard/getSzxxMessageBoardPageLst?&columnId=6787571&pageSize=' \
              '15&pageIndex=' + str(ye) + '&isJson=true&labelName=messageBoardPageList'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.52',
            'Referer': 'http://www.wuhu.gov.cn/zmhd/szxx/index.html',
            'Cookie': 'SHIROJSESSIONID=2036ffcd-0afb-4980-9b90-a1aef36f9416',
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
    create_shizhang()

    for page in range(1, 101):
        try:
            shizhang_data(page)
            print(f'第{page}页读取完毕')
        except Exception as e:
            print('已到达最后一条数据！')
