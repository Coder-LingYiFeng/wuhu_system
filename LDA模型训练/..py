import gensim
import pymysql
import pandas as pd
import jieba
from gensim import corpora, models, similarities

all_zt = ["房屋安置", "修建工程", "孩子学校", "工作工资", "居民户口", "交通", "物业维修", "城市发展", "医疗保险", "公司经营", "补贴政策"]
lda = models.LdaModel.load("./主题分类")
# 做单独每个文档主题
data = pd.read_pickle("content.pickle")
data1 = [data for data in data["contents_clean"]]
# print(data)
dictionary = corpora.Dictionary(data1)
for i in range(10,20):
    bow = dictionary.doc2bow(data.contents_clean[i])   # 数据加入
    print(data.contents_clean[i])
    a = lda.get_document_topics(bow)
    print(all_zt[a[0][0]], a[0][1])
#
# lda = models.LdaModel.load("./主题分类")
# print(lda.print_topics(num_topics=11, num_words=10))
# for year in range(2015, 2021):
#     if year == 2020:
#         lda = models.LdaModel.load(f"./{year}与{year+1}主题分类")
#         print(lda.print_topics(num_topics=11, num_words=10))
#     else:
#         lda = models.LdaModel.load(f"./{year}主题分类")
#         print(lda.print_topics(num_topics=11, num_words=10))

# data =[]
# data1 = []
# for i in range(len(data)):
#     dic1 = {"name": i+2015,
#             "children": data[i]}
#     data1.append(dic1)
# dic = {"name": 2015-2021,
#        "children": data1}
# print(dic)