# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年04月16日
"""
import json

import requests


def get_map_data():
    url = 'http://www.wuhu.gov.cn/site/label/8888?isJson=true&labelName=oneToFiveMessagePm&IsAjax=1&dataType=JSON'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
                      "KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
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
    data_list = []
    for key in XQTop10.keys():
        temp_dict = {"name": key, "value": XQTop10[key]}
        data_list.append(temp_dict)
    print(data_list)
    with open("templates/wuhuData.json", "w", encoding="utf-8") as f:
        json.dump({"datas": data_list}, f)