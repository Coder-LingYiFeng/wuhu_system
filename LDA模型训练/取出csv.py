import pandas as pd
from gensim import corpora

df = pd.read_pickle("content.pickle")
# print(df.contents_clean.tolist())


# def zhuang_str(sj):
#     a = []
#     for i in range(len(sj)):  # 需转成[str，str]
#         b = str(sj[i])[1:-1]
#         a.append(b)
#     return a


# df = zhuang_str(df)
dictionary = corpora.Dictionary(df)
corpus = [dictionary.doc2bow(sentence) for sentence in df]
print(corpus)