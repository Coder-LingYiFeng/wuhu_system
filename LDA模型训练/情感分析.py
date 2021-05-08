import jieba
import os
import pandas as pd
from snownlp import SnowNLP
import pymysql


# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
# vect = CountVectorizer()
# data = pd.read_csv("content.csv")
# print(data.shape)
# data = data.head()['contents_clean']
# print(data[0])

# def get_sentiment(text):
#     return SnowNLP(text).sentiments
#
#
# pre_dict = data.apply(get_sentiment(str(data[0])))
# print(pre_dict)
conn = pymysql.connect(host="localhost", port=3306, user="root",
                       password="123456", database="wuhu", charset="utf8")
sql = "select message from bottom_car"
sql1 = "select message from shizhang"
df = pd.read_sql(sql, conn)
df1 = pd.read_sql(sql1, conn)
df = pd.concat([df, df1], axis=0)
df.index = range(1, len(df)+1)
data = df["message"].sum()
# data = df["message"].apply(lambda x: str(x))
s = SnowNLP(str(data))
print(s.keywords(limit=10))