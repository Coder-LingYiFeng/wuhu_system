from collections import Counter

import pymysql
import json
import pandas as pd
import datetime
import jieba


class all_analyze:
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", port=3306, user="root",
                                    password="123456", database="wuhu", charset="utf8")
        conn = self.conn
        sql = "select * from data_broadcast"
        sql1 = "select * from bottom_car"
        sql2 = "select * from shizhang"
        data1 = pd.read_sql(sql, conn)
        self.data1 = data1
        df = pd.read_sql(sql1, conn)
        df1 = pd.read_sql(sql2, conn)
        data2 = pd.concat([df, df1])
        self.data2 = data2.sort_values(by="year_day", ascending=False)

    def all_data(self):
        data = self.data1
        data = data.all_end.tolist()
        dic1 = {"yuqingshuju": [{"zixun": str(data[0])}, {"qita": str(data[-1])},
                                {"tousu": str(data[1])},
                                {"qiuzhu": str(data[2])}, {"jubao": str(data[3])},
                                {"jianyi": str(data[4])}]}
        return dic1

    def yuqing_zonglang(self):
        data3 = self.data2
        data3["year_day"] = data3["year_day"].apply(lambda x: x.split("-")[0])
        data3 = data3[data3.year_day != "NULL"]
        data3 = data3.groupby(["year_day", "problem_type"]).size().unstack()  # 关于两个列的分组, unstack分组 两个条件作为索引
        data3 = data3.fillna(0)
        dic1 = {"xAxis": data3.index.tolist()}
        series = []
        for i in data3.columns.tolist():
            dic = {"name": i, "data": data3[i].tolist()}
            series.append(dic)
        dic2 = {"yuqingshuliang_zhexiantu": [dic1, {"series": series}]}
        return dic2

    def ciyun(self):
        data = self.data2
        stopwords = pd.read_csv("tyc.csv")
        stopwords = stopwords[stopwords["word"] != "公司"]
        stopwords = stopwords["word"].tolist()
        message = data.message.tolist()
        seg_words = []
        for word in message:
            seg_word = [w for w in jieba.cut(word, cut_all=False) if len(w) > 1 and w not in stopwords]
            seg_words.append(seg_word)
        seg_words = sum(seg_words, [])  # 去除[]
        counter = Counter(seg_words)
        list1 = counter.most_common(8)
        m = []
        for i in range(len(list1)):
            dic = {"name": list1[i][0], "value": list1[i][-1]}
            m.append(dic)
        dic3 = {"yuqiing_reci": m}
        return dic3

    def diqu(self):
        conn = self.conn
        sql = "select * from map_date"
        data = pd.read_sql(sql, conn)
        m = []
        for i in range(len(data)):
            dic = {"name": data.name.tolist()[i], "value": data.value.tolist()[i]}
            m.append(dic)
        dic4 = {"diquxinxi": m}
        return dic4

    def jieshou(self):
        data = self.data2
        data["method"] = data["method"].apply(lambda x: x.split("(")[0])
        data1 = data.groupby("method").size().sort_values(ascending=False)
        del data1["NULL"]
        p = []
        for i in range(len(data1)):
            if data1.values[i] != 0:
                dic = {"value": str(data1.values[i]), "name": data1.index[i]}
                p.append(dic)
        dic5 = {"yuqing_jieshou": p}
        return dic5

    def riqi(self):
        data1 = self.data2
        data1['year_day'] = data1['year_day'].apply(lambda x: x.replace(".", "-").split(" ")[0])
        data1['replyDate'] = data1['replyDate'].apply(lambda x: x.replace(".", "-").split(" ")[0])
        data1 = data1[data1.year_day != "NULL"]
        data1 = data1[data1.replyDate != "NULL"]
        data1["xiangcha"] = data1["replyDate"].apply(pd.to_datetime) - data1["year_day"].apply(pd.to_datetime)  # 日期相减
        data1["xiangcha"] = data1["xiangcha"].apply(lambda x: int(str(x).split(" ")[0]))
        data1 = data1[data1["xiangcha"] > 0]
        date_mean = str(int(data1["xiangcha"].mean())) + "天"
        date_max = str(data1["xiangcha"].max()) + "天"
        date_min = str(data1["xiangcha"].min()) + "天"
        dic1 = {
            "chulitianshu": [{"pinjuntianshu": date_mean}, {"zuidatianshu": date_max}, {"zuixiaotianshu": date_min}]}
        data2 = data1.groupby("xiangcha").size()
        data2.index = data2.index.map(lambda x: str(x) + "天")
        dic2 = {"time_zhuxingtu": [{"xAxis": {"type": 'category', "data": data2.index.tolist()}},
                                   {"series": [
                                       {"name": "受理时间", "type": "bar", "data": data2.values.tolist()}]}]}
        dic6 = {"chulishijian": [dic1, dic2]}
        return dic6


a = all_analyze()
dic = {"zongfenxi": [a.riqi(), a.all_data(), a.yuqing_zonglang(), a.ciyun(), a.diqu(), a.jieshou()]}
with open("templates/yuqingzonglan.json", "w") as f:
    json.dump(dic, f)
