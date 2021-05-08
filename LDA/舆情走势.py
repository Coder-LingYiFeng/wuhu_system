import json

import pandas as pd
import pymysql
from gensim import corpora, models
import jieba

zhutis = [["城市建设", "拆迁工程", "孩子学校", "工作工资", "生活政策"], ["房屋拆迁", "经济发展", "补贴政策", "工作生活", "居民安置"],
         ["工作", "物业", "拆迁", "环境", "买房"], ["物业", "拆迁", "工程影响", "居民安置", "工作"], ["农业", "环境", "物业", "交通", "拆迁"],
         ["工程修建", "医疗疫情", "政策补贴", "教育", "工作"]]


def zhu_ti(year):
    conn = pymysql.connect(host="localhost", port=3306, user="root",
                           password="123456", database="wuhu", charset="utf8")
    sql = f'select * from bottom_car where year_day like "{year}%"'
    sql1 = f'select * from shizhang where year_day like "{year}%"'
    df = pd.read_sql(sql, conn)
    df1 = pd.read_sql(sql1, conn)
    df = pd.concat([df, df1], axis=0).sort_values(by="year_day", ascending=False)
    data1 = df.copy()
    if year == 2021:
        year = 2020
    zhuti = zhutis[year-2015]
    lda = models.LdaModel.load(f"document\{year}主题分类")
    data = pd.read_pickle(f"document\{year}content.pickle")
    data = [data for data in data["contents_clean"]]
    dictionary = corpora.Dictionary(data)
    stopwords = pd.read_csv("tyc.csv")
    stopwords = stopwords["word"].tolist()
    w = []
    for i in range(len(data1)):
        seg_word = [w for w in jieba.cut(data1["message"].tolist()[i],
                                         cut_all=False) if len(w) > 1 and w not in stopwords]
        bow = dictionary.doc2bow(seg_word)
        a = lda.get_document_topics(bow)
        b = [i[1] for i in a]
        b.sort(reverse=True)
        for z in a:
            if b[0] == z[1]:
                z_t = z[0]
                w.append(zhuti[z_t])
    data1["zhuti"] = w
    data1.year_day = data1.year_day.apply(lambda x: x.replace(".", "-")[0:7])
    re_dian = data1.groupby("zhuti").size()
    m = []
    for i in range(len(re_dian)):
        dic = {"name": re_dian.index.tolist()[i], "value": re_dian.values.tolist()[i]}
        m.append(dic)
    dic1 = {"yuqing_wenzibintu": m}
    zou_shi = data1.groupby(["year_day", "zhuti"]).size().unstack()
    zou_shi = zou_shi.fillna(0)
    dic2 = {"xAxis": zou_shi.index.tolist()}
    series = []
    for i in zou_shi.columns.tolist():
        dic = {"name": i, "data": zou_shi[i].tolist()}
        series.append(dic)
    dic3 = {"yuqingzoushi": [dic2, {"series": series}]}
    dic = {"lda_shuju": [dic1, dic3]}
    return dic


for a in range(2015, 2022):
    datas = zhu_ti(a)
    print(datas)
    with open(f"../templates/LDA_{a}.json", "w") as f:
        json.dump(datas, f)
