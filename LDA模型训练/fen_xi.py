import gensim
import pymysql
import pandas as pd
import jieba
from gensim import corpora, models, similarities
lda = models.LdaModel.load("./主题分类")
all_zt = ["学校教育", "环境建设", "燃气问题", "工作工资", "医疗", "社会保险", "物业维修", "基础设施", "社会政策", "交易服务", "补贴政策"]
# all_zt = ["学校教育", "工程建设", "燃气问题", "工作工资", "道路交通", "交通", "物业维修", "基础设施", "医疗保险", "公司经营", "补贴政策"]
# all_zt = ["房屋安置", "修建工程", "孩子学校", "工作工资", "居民户口", "交通", "物业维修", "城市发展", "医疗保险", "公司经营", "补贴政策"]
# 做单独每个文档主题
data = pd.read_pickle("content.pickle")
conn = pymysql.connect(host="localhost", port=3306, user="root",
                       password="123456", database="wuhu", charset="utf8")
sql = f'select * from bottom_car'
sql1 = f'select * from shizhang'
df = pd.read_sql(sql, conn)
df1 = pd.read_sql(sql1, conn)
df = pd.concat([df, df1], axis=0)
df.index = range(0, len(df))
df["message"] = data
df = df.sort_values(by="year_day", ascending=False)
df = df[df["year_day"] != "NULL"]
df.index = range(0, len(df))
df.id = range(1, len(df)+1)
print(df.columns)
# data1 = [data for data in data["contents_clean"]]
# dictionary = corpora.Dictionary(data1)
# for i in range(100, 1000):
#     bow = dictionary.doc2bow(data.contents_clean[i])   # 数据加入
#     a = lda.get_document_topics(bow)
#     if len(a) > 2 and a[0][1] != a[1][1]:
#         continue
#     elif a[0][1] > 0.9:
#         print(data.contents_clean[i])
#         print(all_zt[a[0][0]], a[0][1])