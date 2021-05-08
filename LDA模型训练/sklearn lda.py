from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
from sklearn.externals import joblib
from nltk.stem.porter import PorterStemmer

data = pd.read_pickle("content.pickle")
data1 = [data for data in data["contents_clean"]]
cntVector = CountVectorizer(max_df=0.5, min_df=10)


def zhuang_str(sj):
    a = []
    for i in range(len(sj)):  # 需转成[str，str]
        b = str(sj[i])[1:-1]
        a.append(b)
    return a


data1 = zhuang_str(data1)
cntTf = cntVector.fit_transform(data1)
lda = LatentDirichletAllocation(n_topics=11,
                                learning_offset=50.,
                                random_state=0)


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):

        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

    print(model.components_)


n_top_words = 20
tf_feature_names = cntVector.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)