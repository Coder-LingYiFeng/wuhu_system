import json
import sys
import os
import gensim
import pymysql
import pandas as pd
import jieba
from gensim import corpora, models, similarities

import_dir = \
    os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), 'zhu_ti')
sys.path.insert(0, import_dir)


def fl_year():
    lda = models.LdaModel.load("./主题分类")
    conn = pymysql.connect(host="localhost", port=3306, user="root",
                           password="123456", database="wuhu", charset="utf8")
    all_zt = ["房屋安置", "修建工程", "孩子学校", "工作工资", "居民户口", "交通", "物业维修", "城市发展", "医疗保险", "公司经营", "补贴政策"]
    data2 = []

    def year_yuqing(date):
        sql = f'select * from bottom_car where year_day like "{date}%"'
        sql1 = f'select * from shizhang where year_day like "{date}%"'
        df = pd.read_sql(sql, conn)
        df1 = pd.read_sql(sql1, conn)
        df = pd.concat([df, df1], axis=0)
        # print(df.columns)
        data = df["message"].tolist()
        seg_words = []
        for word in data:
            seg_word = [w for w in jieba.cut(word, cut_all=False) if len(w) > 1]
            seg_words.append(seg_word)
        # print(seg_words)
        df_seg = pd.DataFrame({"content": seg_words})
        return df_seg, data

    def drop_stopwords(stopwords1, date1):
        df_seg, df = year_yuqing(date1)
        contents = df_seg.content.values.tolist()
        stopwords1 = stopwords1.stopword.values.tolist()
        contents_clean1 = []
        all_words1 = []
        for line in contents:
            line_clean = []
            for word in line:
                if word in stopwords1:
                    continue
                line_clean.append(word)
                all_words1.append(word)
            contents_clean1.append(line_clean)
        return contents_clean1, all_words1, df

    for year in range(2015, 2022):
        stopwords = pd.read_csv("tyc.csv")
        stopwords = stopwords["word"].tolist()
        stopwords = pd.DataFrame({"stopword": stopwords})
        contents_clean, all_words, df = drop_stopwords(stopwords, year)
        data = pd.read_pickle("content.pickle")
        data1 = [data for data in data["contents_clean"]]
        dictionary = corpora.Dictionary(data1)  # 需要求大于他的语料库  data1 为总的预料库
        bow = dictionary.doc2bow(all_words)
        # bow = dictionary.doc2bow(contents_clean[3])
        # print(contents_clean[3])
        a = lda.get_document_topics(bow)
        b = [i[1] for i in a]
        b.sort(reverse=True)
        zhu_ti = []
        gai_lv = b[0:3]
        for i in range(3):
            for z in a:
                if b[i] == z[1]:
                    zhu_ti.append(z[0])
        # print(zhu_ti)
        # print(gai_lv)
        datas = []
        for i in range(3):
            # temp_dict = {'name': zhu_ti[i], 'value': gai_lv[i]}
            temp_dict = {'name': all_zt[zhu_ti[i]], 'value': gai_lv[i]}
            datas.append(temp_dict)
        print(datas)
        print(f"{year}年完成")
        data2.append(datas)
    data1 = []
    for i in range(len(data2)):
        dic1 = {"name": i + 2015,
                "children": data2[i]}
        data1.append(dic1)
    dic = {"name": "2015-2021",
           "children": data1}
    with open('all.json', 'w') as f:
        f.write(json.dumps({"datas": str(dic)}))
    # print(dic)


fl_year()
