import gensim
import pymysql
import pandas as pd
import jieba
from wordcloud import STOPWORDS
import numpy as np
from gensim import corpora, models, similarities

conn = pymysql.connect(host="localhost", port=3306, user="root",
                       password="123456", database="wuhu", charset="utf8")


def year_yuqing(date1):
    if date1 == 0:
        sql = "select * from bottom_car"
        sql1 = "select * from shizhang"
        df = pd.read_sql(sql, conn)
        df1 = pd.read_sql(sql1, conn)
        df = pd.concat([df, df1], axis=0)
        data = df["message"].tolist()
        seg_words = []
        for word in data:
            seg_word = [w for w in jieba.cut(word, cut_all=False) if len(w) > 1]
            seg_words.append(seg_word)
        df_seg = pd.DataFrame({"content": seg_words})
        return df_seg
    sql = f'select * from bottom_car where year_day like "{date1}%"'
    sql1 = f'select * from shizhang where year_day like "{date1}%"'
    df = pd.read_sql(sql, conn)
    df1 = pd.read_sql(sql1, conn)
    df = pd.concat([df, df1], axis=0)
    data = df["message"].tolist()
    seg_words = []
    for word in data:
        seg_word = [w for w in jieba.cut(word, cut_all=False) if len(w) > 1]
        seg_words.append(seg_word)
    # print(len(sum(seg_words, [])))   # 检查去除停用词是否成功
    df_seg = pd.DataFrame({"content": seg_words})
    return df_seg


def drop_stopwords(stopwords, date):
    contents = year_yuqing(date).content.values.tolist()
    stopwords = stopwords.stopword.values.tolist()
    contents_clean = []
    all_words = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords:
                continue
            line_clean.append(word)
            all_words.append(word)
        contents_clean.append(line_clean)
    return contents_clean, all_words


for year in range(2020, 2021):
    stopwords = pd.read_csv("tyc.csv")
    stopwords = stopwords["word"].tolist()
    stopwords = pd.DataFrame({"stopword": stopwords})
    contents_clean, all_words = drop_stopwords(stopwords, 0)   # contents_clean短文本，all_words所有加起来总文本
    # print(len(all_words))   # 检查去除停用词是否成功
    df_content = pd.DataFrame({"contents_clean": contents_clean})
    df_all_words = pd.DataFrame({"all_words": all_words})
    dictionary = corpora.Dictionary(contents_clean)
    df_content.to_pickle(f"{year}content.pickle")
    corpus = [dictionary.doc2bow(sentence) for sentence in contents_clean]
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=11, random_state=3)
    print(lda.print_topics(num_topics=5, num_words=10))
    lda.save(f"./{year}主题分类")
    print("模型保存完成")

