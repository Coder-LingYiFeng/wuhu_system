import pandas as pd
import matplotlib.pyplot as plt
import pymysql
import jieba

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import random
from time import time

conn = pymysql.connect(host="localhost", port=3306, user="root",
                       password="123456", database="wuhu", charset="utf8")
sql = f'select * from bottom_car where year_day'
sql1 = f'select * from shizhang where year_day'
df = pd.read_sql(sql, conn)
df1 = pd.read_sql(sql1, conn)
df = pd.concat([df, df1], axis=0)
data = df["message"].tolist()
seg_words = []
for word in data:
    seg_word = [w for w in jieba.cut(word, cut_all=False) if len(w) > 1]
    seg_words.append(seg_word)
stopwords = pd.read_csv("tyc.csv")
stopwords = stopwords["word"].tolist()
# a = sum(seg_words, [])
# print(len(a))
content_clean = []
for line in seg_words:
    line_clean = []
    for word in line:
        if word not in stopwords:
            line_clean.append(word)
    content_clean.append(line_clean)
print("*****************")
# texts = sum(content_clean, [])
# print(len(texts))
bow_corpus = []
for trace in content_clean:
    bow_corpus.append(trace)
train_size = int(round(len(bow_corpus) * 0.8))
# print(train_size)   ###分解训练集和测试集
train_index = sorted(random.sample(range(len(bow_corpus)), train_size))  # 随机选取下标
test_index = sorted(set(range(len(bow_corpus))) - set(train_index))
train_corpus = [bow_corpus[i] for i in train_index]
test_corpus = [bow_corpus[j] for j in test_index]
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.5, min_df=10)  # 选取至少出现过十次
t0 = time()


def zhuang_str(sj):
    a = []
    for i in range(len(sj)):  # 需转成[str，str]
        b = str(sj[i])[1:-1]
        a.append(b)
    return a


train_corpus = zhuang_str(train_corpus)
test_corpus = zhuang_str(test_corpus)
# print(len(train_corpus))
# print(len(test_corpus))
tf = tf_vectorizer.fit_transform(train_corpus)  # 使用向量生成器转化测试集
print("done in %0.3fs." % (time() - t0))
# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_test = tf_vectorizer.transform(test_corpus)
print("done in %0.3fs." % (time() - t0))
grid = dict()
t0 = time()
for i in range(1, 20, 1):  # 20个主题，以1为间隔
    grid[i] = list()
    n_topics = i

    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5, learning_method='online', learning_offset=50.,
                                    random_state=0)  # 定义lda模型
    lda.fit(tf)  # 训练参数
    train_gamma = lda.transform(tf)  # 得到topic-document 分布
    train_perplexity = lda.perplexity(tf)
    test_perplexity = lda.perplexity(tf_test)  # s计算测试集困惑度
    print('sklearn preplexity: train=%.3f' % (train_perplexity))

    grid[i].append(train_perplexity)

print("done in %0.3fs." % (time() - t0))
df = pd.DataFrame(grid)
# df.to_csv('sklearn_perplexity.csv')
print(df)
plt.figure(figsize=(14, 8), dpi=120)
# plt.subplot(221)
plt.plot(df.columns.values, df.iloc[0].values, '#007A99')
plt.xticks(df.columns.values)
plt.ylabel('train Perplexity')
plt.show()
# plt.savefig('lda_topic_perplexity.png', bbox_inches='tight', pad_inches=0.1)
