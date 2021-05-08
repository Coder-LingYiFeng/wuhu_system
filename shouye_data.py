import pymysql
import json
import pandas as pd
import datetime
import jieba
from collections import Counter


class first_page:
    def __init__(self):
        stopwords = pd.read_csv("tyc.csv")
        stopwords = stopwords["word"].tolist()
        self.stopwords = stopwords
        self.conn = pymysql.connect(host="localhost", port=3306, user="root",
                                    password="123456", database="wuhu", charset="utf8")
        conn = self.conn
        sql = f" select * from bottom_car"
        data = pd.read_sql(sql, conn)
        data.year_day = data.year_day.apply(lambda x: x.replace(".", "-"))
        data = data[data.year_day != "NULL"]
        data.year_day = data.year_day.apply(pd.to_datetime)
        b = data.year_day[0] - datetime.timedelta(7)
        d = b - datetime.timedelta(7)
        con1 = data.year_day <= data.year_day[0]
        con2 = data.year_day > b
        con3 = data.year_day <= b
        con4 = data.year_day > d
        data1 = data[con1 & con2]
        data2 = data[con3 & con4]
        self.data1 = data1
        self.data2 = data2

    def ben_zhou(self):
        data = self.data1
        problem = data.groupby("problem_type").size()
        z_l = ["我要咨询", "其他", "我要投诉", "我要求助", "我要举报", "我要建议"]
        for i in z_l:
            if i not in problem.index:
                problem[i] = 0
        dic1 = {"baodaotongji": [{"zixun": str(problem["我要咨询"])}, {"qita": str(problem["其他"])},
                                 {"tousu": str(problem["我要投诉"])},
                                 {"qiuzhu": str(problem["我要求助"])}, {"jubao": str(problem["我要举报"])},
                                 {"jianyi": str(problem["我要建议"])}]}
        p = []
        for i in range(len(problem)):
            if problem.values[i] != 0:
                dic = {"value": str(problem.values[i]), "name": problem.index[i]}
                p.append(dic)
        dic2 = {"shijianzhonglei_bingtu": p}
        method = data.groupby("method").size().sort_values(ascending=False)
        if "NULL" in data.index:
            data = data.drop("NULL")
        dic3 = {"fangfa_zhuxingtu": [{"yAxis": {"type": 'category', "data": method.index.tolist()}},
                                     {"series": [
                                         {"name": "舆情来源", "type": "bar", "data": method.values.tolist()}]}]}
        stopwords = self.stopwords
        message = data.message.tolist()
        seg_words = []
        for word in message:
            seg_word = [w for w in jieba.cut(word, cut_all=False) if len(w) > 1 and w not in stopwords]
            seg_words.append(seg_word)
        seg_words = sum(seg_words, [])  # 去除[]
        counter = Counter(seg_words)
        list1 = counter.most_common(len(counter))
        m = []
        for i in range(len(list1)):
            dic = {"name": list1[i][0], "value": list1[i][-1]}
            m.append(dic)
        dic4 = {"ciyunshuju": m}
        dic = {"benzhoushuju": [dic1, dic2, dic3, dic4]}
        return dic

    def shang_zhou(self):
        data = self.data2
        problem = data.groupby("problem_type").size()
        z_l = ["我要咨询", "其他", "我要投诉", "我要求助", "我要举报", "我要建议"]
        for i in z_l:
            if i not in problem.index:
                problem[i] = 0
        dic1 = {"baodaotongji": [{"zixun": str(problem["我要咨询"])}, {"qita": str(problem["其他"])},
                                 {"tousu": str(problem["我要投诉"])},
                                 {"qiuzhu": str(problem["我要求助"])}, {"jubao": str(problem["我要举报"])},
                                 {"jianyi": str(problem["我要建议"])}]}
        stopwords = self.stopwords
        message = data.message.tolist()
        seg_words = []
        for word in message:
            seg_word = [w for w in jieba.cut(word, cut_all=False) if len(w) > 1 and w not in stopwords]
            seg_words.append(seg_word)
        seg_words = sum(seg_words, [])  # 去除[]
        counter = Counter(seg_words)
        list1 = counter.most_common(len(counter))
        m = []
        for i in range(len(list1)):
            dic = {"name": list1[i][0], "value": list1[i][-1]}
            m.append(dic)
        dic2 = {"ciyunshuju": m}
        dic = {"shangzhoushuju": [dic1, dic2]}
        return dic


def run():
    a = first_page()
    data = {"shouyeshuju": [a.ben_zhou(), a.shang_zhou()]}
    with open("templates/shouye.json", "w") as f:
        json.dump(data, f)


run()
