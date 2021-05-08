# -*-coding:utf-8-*-
"""
作者：LYF
日期：2020年12月05日
"""
import requests
import json
from sql_data_broadcast import *


def modular_three():
    creat_data_broadcast()
    url = 'http://www.wuhu.gov.cn/site/label/8888?isJson=true&labelName=oneToFiveDataBroadcast'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.42'
                      '80.67Safari/537.36 Edg/87.0.664.55',
        'Referer': 'http://www.wuhu.gov.cn/zmhd/index.html',
        'Host': 'www.wuhu.gov.cn',
        'Cookie': 'SHIROJSESSIONID=eaf6f950-03a2-4b66-96a5-baddf483a599',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.get(url=url, headers=headers, timeout=10).json()
    response_dict = json.loads(response)
    data_dict = response_dict['obj']  # 取obj对应的值
    zixun = ['咨询']  # 用于保存咨询一行的数据
    tousu = ['投诉']  # 用于保存投诉一行的数据
    qiuzhu = ['求助']  # 用于保存求助一行的数据
    jubao = ['举报']  # 用于保存举报一行的数据
    jianyi = ['建议']  # 用于保存建议一行的数据
    qita = ['其他']  # 用于保存其他一行的数据
    shu_title_list = [zixun, tousu, qiuzhu, jubao, jianyi, qita]  # 用于遍历上述保存数据的列表
    shu_title = ['咨询', '投诉', '求助', '举报', '建议', '其他']  # 用于遍历生成字典键
    time_title = ['当日', '当月', '年度', '年度总']  # 用于遍历生成字典键
    leixin_title = ['受理量', '办结量']  # 用于遍历生成字典键
    for title in shu_title:
        for time in time_title:
            for leixin in leixin_title:
                if title == '咨询':
                    zixun.append(data_dict[f'{title}{time}{leixin}'])  # 追加数据到列表
                elif title == '投诉':
                    tousu.append(data_dict[f'{title}{time}{leixin}'])  # 追加数据到列表
                elif title == '求助':
                    qiuzhu.append(data_dict[f'{title}{time}{leixin}'])  # 追加数据到列表
                elif title == '举报':
                    jubao.append(data_dict[f'{title}{time}{leixin}'])  # 追加数据到列表
                elif title == '建议':
                    jianyi.append(data_dict[f'{title}{time}{leixin}'])  # 追加数据到列表
                elif title == '其他':
                    qita.append(data_dict[f'{title}{time}{leixin}'])  # 追加数据到列表
    # 将数据存入sql
    print(shu_title_list)
    for line in shu_title_list:
        sql_write(line)
    print('写入数据完成！')
