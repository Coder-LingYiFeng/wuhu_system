import json

import pymysql
import pandas as pd
import jieba
from gensim import corpora, models

conn = pymysql.connect(host="localhost", port=3306, user="root",
                       password="123456", database="wuhu", charset="utf8")
data3 = [["城市建设", "拆迁工程", "孩子学校", "工作工资", "生活政策"], ["房屋拆迁", "经济发展", "补贴政策", "工作生活", "居民安置"],
         ["工作", "物业", "拆迁", "环境", "买房"], ["物业", "拆迁", "工程影响", "居民安置", "工作"], ["农业", "环境", "物业", "交通", "拆迁"],
         ["工程修建", "医疗疫情", "政策补贴", "教育", "工作"]]


def year_yu_qing(date):
    sql = f'select * from bottom_car where year_day like "{date}%"'
    sql1 = f'select * from shizhang where year_day like "{date}%"'
    df = pd.read_sql(sql, conn)
    df1 = pd.read_sql(sql1, conn)
    df = pd.concat([df, df1], axis=0)
    data2 = df["message"].tolist()
    seg_words = []
    for word in data2:
        seg_word = [w for w in jieba.cut(word, cut_all=False) if len(w) > 1]
        seg_words.append(seg_word)
    df_seg = pd.DataFrame({"content": seg_words})
    return df_seg


def drop_stopwords(stopwords1, date1):
    contents = year_yu_qing(date1).content.values.tolist()
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
    return contents_clean1, all_words1


for year in range(2015, 2021):
    data6 = []
    data4 = data3[year - 2015]
    if year == 2020:
        lda = models.LdaModel.load(f"./{year}与{year + 1}主题分类")
        for s in range(1, 16):
            stopwords = pd.read_csv("tyc.csv")
            stopwords = stopwords["word"].tolist()
            stopwords = pd.DataFrame({"stopword": stopwords})
            if 9 < s < 13:
                d = float(str(year) + "." + str(s))
            elif s < 10:
                d = float(str(year) + ".0" + str(s))
            else:
                d = float(str(year + 1) + ".0" + str(s - 12))
            contents_clean, all_words = drop_stopwords(stopwords, d)
            data = pd.read_pickle(f"{year}与{year + 1}content.pickle")
            data1 = [data for data in data["contents_clean"]]
            dictionary = corpora.Dictionary(data1)                 # 为当年的语料库
            bow = dictionary.doc2bow(all_words)
            a = lda.get_document_topics(bow)
            b = [i[1] for i in a]
            b.sort(reverse=True)
            zhu_ti = []
            gai_lv = b[0:len(b)]
            for i in range(len(b)):
                if i < 3:
                    for z in a:
                        if b[i] == z[1]:
                            zhu_ti.append(z[0])
            datas = []
            for i in range(len(zhu_ti)):
                temp_dict = {'name': data4[zhu_ti[i]], 'value': gai_lv[i]}
                datas.append(temp_dict)
            # print(datas)
            data6.append(datas)
            if s > 12:
                print(f"{year + 1}第{s - 12}月完成")
            else:
                print(f"{year}第{s}月完成")
    else:
        lda = models.LdaModel.load(f"./{year}主题分类")
        for s in range(1, 13):
            stopwords = pd.read_csv("tyc.csv")
            stopwords = stopwords["word"].tolist()
            stopwords = pd.DataFrame({"stopword": stopwords})
            if s > 9:
                d = float(str(year) + "." + str(s))
            else:
                d = float(str(year) + ".0" + str(s))
            contents_clean, all_words = drop_stopwords(stopwords, d)
            if len(contents_clean) == 0:
                data6.append([])
                continue
            data = pd.read_pickle(f"{year}content.pickle")
            data1 = [data for data in data["contents_clean"]]
            dictionary = corpora.Dictionary(data1)               # 为当年的语料库
            bow = dictionary.doc2bow(all_words)
            a = lda.get_document_topics(bow)
            b = [i[1] for i in a]
            b.sort(reverse=True)
            zhu_ti = []
            gai_lv = b[0:len(b)]
            for i in range(len(b)):
                if i < 3:
                    for z in a:
                        if b[i] == z[1]:
                            zhu_ti.append(z[0])
            datas = []
            for i in range(len(zhu_ti)):
                temp_dict = {'name': data4[zhu_ti[i]], 'value': gai_lv[i]}
                datas.append(temp_dict)
            # print(datas)
            print(f"{year}第{s}月完成")
            data6.append(datas)
# print(len(data5[5]))
    # 写入json格式
    year_month1 = []
    year_month2 = []
    for i in range(len(data6)):
        dic1 = {"name": f"{i+1}月", "children": data6[i]}
        if i > 11:
            dic2 = {"name": f"{i-11}月", "children": data6[i]}
            year_month2.append(dic2)
            dic2 = {"name": year + 1, "children": year_month2}
            with open(f'第{year + 1}.json', 'w') as f:
                f.write(json.dumps({"datas": str(dic2)}))
        year_month1.append(dic1)
    dic = {"name": year, "children": year_month1}
    with open(f'第{year}.json', 'w') as f:
        f.write(json.dumps({"datas": str(dic)}))
