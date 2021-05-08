import threading

import pymysql
import json
import pandas as pd
from gensim import corpora, models
import jieba


class Picture:
    def __init__(self, keyword):
        self.conn = pymysql.connect(host="localhost", port=3306, user="root",
                                    password="123456", database="wuhu", charset="utf8")
        conn = pymysql.connect(host="localhost", port=3306, user="root",
                               password="123456", database="wuhu", charset="utf8")
        sql = f'select * from bottom_car where message like "%{keyword}%"'
        sql1 = f'select * from shizhang where message like "%{keyword}%"'
        df = pd.read_sql(sql, conn)
        df1 = pd.read_sql(sql1, conn)
        df = pd.concat([df, df1], axis=0)
        self.number = len(df)
        data = df.sort_values(by="year_day", ascending=False)
        if len(data) != 0:
            self.data = data

    # 生成第一个数据（地区以及时间的信息，还有问题种类）
    def time_area(self):
        # 事件初始以及末尾发生地区和时间
        qu_xian = ["鸠江", "镜湖", "弋江", "繁昌", "湾沚", "南陵", "无为", "芜湖县", "三山"]
        data = self.data[["year_day", "receiveunitname", "message", "problem_type"]]
        first_time = data["year_day"].tolist()[-1]  # 第一次发生的时间
        last_time = data["year_day"].tolist()[0]  # 最后一次发生的时间
        first_area = [i for i in qu_xian if i in data.message.tolist()[-1]]  # 第一次发生的地区
        if len(first_area) != 0:
            first_area = first_area[0]
        last_area = [i for i in qu_xian if i in data.message.tolist()[0]]  # 最后一次发生的地区
        if len(last_area) != 0:
            last_area = last_area[0]
        if not first_area:
            first_area = data.receiveunitname.tolist()[-1]
            if first_area == "暂无接收单位":
                first_area = "未知"
            elif len(first_area) > 6:
                for i in range(len(data.message.tolist())):
                    for a in qu_xian:
                        if a in data.message.tolist()[i]:
                            first_area = a
                            break
                    else:
                        continue
                    break
        if not last_area:
            last_area = data.receiveunitname.tolist()[0]
            if last_area == "暂无接收单位":
                last_area = "未知"
            elif len(last_area) > 6:
                for i in range(len(data.message.tolist())):
                    for a in qu_xian:
                        if a in data.message.tolist()[i]:
                            last_area = a
                            break
                    else:
                        continue
                    break
        dic1 = {"chushimowei": [{"first_time": first_time.split(" ")[0]}, {"first_area": first_area},
                                {"last_time": last_time.split(" ")[0]}, {"last_area": last_area}]}
        # 事件爆发时间以及数量
        year_month = data.year_day.map(lambda x: x[0:7])
        year_month = pd.DataFrame(year_month)
        tong_ji = year_month.groupby("year_day").size()
        sort_tong_ji = tong_ji.sort_values(ascending=False)  # 排序爆发数量 取最多的数量
        break_time = sort_tong_ji.index[0]  # 爆发月份
        message = sort_tong_ji.values[0]  # 文章数量
        dic2 = {"shijianbaofa": [{"baofayuefen": break_time}, {"wenzhangshuliang": str(message)}]}
        # 事件报道统计
        problem = data.groupby("problem_type").size().sort_values(ascending=False)  # 排序后的问题种类
        z_l = ["我要咨询", "其他", "我要投诉", "我要求助", "我要举报", "我要建议"]
        for i in z_l:
            if i not in problem.index:
                problem[i] = 0
        dic3 = {"baodaotongji": [{"zixun": str(problem["我要咨询"])}, {"qita": str(problem["其他"])},
                                 {"tousu": str(problem["我要投诉"])},
                                 {"qiuzhu": str(problem["我要求助"])}, {"jubao": str(problem["我要举报"])},
                                 {"jianyi": str(problem["我要建议"])}]}
        # 事件接受分布(折线图)
        index = tong_ji.index.tolist()
        values = tong_ji.values.tolist()
        dic4 = {"shijianjieshou_zhexiantu": [{"xAxis": index, "series": values}]}
        # 事件答复单位分布（漏斗图）
        reply = data.groupby("receiveunitname").size().sort_values(ascending=False)
        if "暂无接收单位" in reply.index:
            reply = reply.drop("暂无接收单位")
        reply = reply[reply.values > 1]
        r = []
        for i in range(len(reply)):
            dic = {"value": str(reply.values[i]), "name": reply.index[i]}  # 答复单位的字典数据
            r.append(dic)
        dic5 = {"shijiandafudanwei_loudoutu": [{"max": reply.values.tolist()[0]}, {"data": r}]}

        # 事件种类分布
        p = []
        for i in range(len(problem)):
            if problem.values[i] != 0:
                dic = {"value": str(problem.values[i]), "name": problem.index[i]}
                p.append(dic)
        dic6 = {"shijianzhonglei_bingtu": p}
        dic = {"jianyaofenxi": [dic1, dic2, dic3, dic4, dic5, dic6]}
        return dic

    def bin_tu(self):
        data = self.data
        data = data.groupby("method").size().sort_values(ascending=False)
        if "NULL" in data.index:
            data = data.drop("NULL")
        m = []
        for i in range(len(data)):
            dic = {"value": str(data.values[i]), "name": data.index[i]}
            m.append(dic)
        dic = {"shijianbaodao_bingtu": m}
        return dic

    def influence(self):  # 事件影响 需要用到LDA
        global zhu_ti
        all_zt = ["房屋安置", "修建工程", "孩子学校", "工作工资", "居民户口", "交通", "物业维修", "城市发展", "医疗保险", "公司经营", "补贴政策"]
        lda = models.LdaModel.load("./主题分类")
        data = self.data
        data1 = pd.read_pickle("content.pickle")
        data2 = [data for data in data1["contents_clean"]]
        dictionary = corpora.Dictionary(data2)
        stopwords = pd.read_csv("tyc.csv")
        stopwords = stopwords["word"].tolist()
        w = []
        for i in data["message"].tolist():
            seg_word = [w for w in jieba.cut(i, cut_all=False) if len(w) > 1 and w not in stopwords]
            bow = dictionary.doc2bow(seg_word)  # 数据加入
            a = lda.get_document_topics(bow)
            b = [i[1] for i in a]
            b.sort(reverse=True)
            for z in a:
                if b[0] == z[1]:
                    zhu_ti = z[0]
            w.append(all_zt[zhu_ti])
        w = pd.Series(w)
        w = w.value_counts()
        if len(w) > 10:
            dic = {"shijianyingxiang_zhuxingtu": [{"xAxis": {"type": 'category', "data": w.index.tolist()[0:10]}},
                                                  {"series": [{"name": "影响主题", "data": w.values.tolist()[0:10],
                                                               "type": 'bar'}]}]}
        else:
            dic = {"shijianyingxiang_zhuxingtu": [{"xAxis": {"type": 'category', "data": w.index.tolist()}},
                                                  {"series": [{"name": "影响主题", "data": w.values.tolist(),
                                                               "type": 'bar'}]}]}
        return dic

    def attention(self):  # 网民关注度分析
        data = self.data
        data = data.year_day.map(lambda x: x.split(" ")[0][0:7])
        data = data.value_counts()
        break_time = data.index.tolist()[0]
        message1 = data[break_time]
        conn = self.conn
        sql = f'select * from bottom_car where year_day like "{break_time}%"'
        sql2 = f'select * from shizhang where year_day like "{break_time}%"'
        data1 = pd.read_sql(sql, conn)
        data2 = pd.read_sql(sql2, conn)
        data3 = pd.concat([data1, data2], axis=0)
        a = int(message1) / len(data3) + 0.25
        a = ("%.2f" % a)
        tu_data = [{"value": a, "name": "程度分析"}]  # 等级仪表盘 data的数据
        dic = {"yibiaotu": {"data": tu_data}}
        return dic

    def reply(self):  # 政府反馈信息报道
        data = self.data
        data['year_day'] = data['year_day'].apply(lambda x: x.replace(".", "-").split(" ")[0])
        data['replyDate'] = data['replyDate'].apply(lambda x: x.replace(".", "-").split(" ")[0])
        data["xiangcha"] = data["replyDate"].apply(pd.to_datetime) - data["year_day"].apply(pd.to_datetime)  # 日期相减
        data["xiangcha"] = data["xiangcha"].apply(lambda x: int(x.days))
        data = data[data["xiangcha"] >= 0]
        date = data["xiangcha"].sort_values(ascending=False)
        mean_date = str(int(date.mean())) + "天"
        long_date = str(date.values.tolist()[0]) + "天"
        short_date = str(date.values.tolist()[-1]) + "天"
        if short_date == "0天":
            short_date = "当天"
        dic1 = {"wengzixinxi": [{"chulishijian": [{"short_date": short_date}, {"long_date": long_date},
                                                  {"mean_date": mean_date}]}, {"manyidu": "100%"}]}
        data1 = data.groupby("xiangcha").size()
        data1.index = data1.index.map(lambda x: str(x) + "天")  # 单独的一个series要用map
        if len(data1) > 15:
            dic2 = {"time_zhuxingtu": [{"yAxis": {"type": 'category', "data": data1.index.tolist()[0:15]}},
                                       {"series": [{"name": "受理时间", "type": "bar",
                                                    "data": data1.values.tolist()[0:15]}]}]}
        else:
            dic2 = {"time_zhuxingtu": [{"yAxis": {"type": 'category', "data": data1.index.tolist()}},
                                       {"series": [
                                           {"name": "受理时间", "type": "bar", "data": data1.values.tolist()}]}]}
        data = data.copy()
        data["xiangcha"] = data["xiangcha"].apply(lambda x: str(x) + "天")
        data = data.groupby("xiangcha").size().sort_values(ascending=False)
        m = []
        for i in range(len(data)):
            if i < 13:
                dic = {"value": str(data.values[i]), "name": data.index[i]}
                m.append(dic)
        dic3 = {"time_bingtu": m}
        dic = {"zhengfufankui": [dic1, dic2, dic3]}
        return dic


def cha_xun(keyword1):
    shi_jiang = Picture(keyword1)
    # print(shi_jiang.__dict__)  # 查看初始化是否成功(数据库查询数据是否存在)
    if shi_jiang.__dict__ == {} or shi_jiang.number < 5:
        print("查询信息太少！")
        return json.loads("templates/yiqing_error.json")
    s = [shi_jiang.time_area, shi_jiang.bin_tu, shi_jiang.influence, shi_jiang.attention, shi_jiang.reply]

    class MyThread(threading.Thread):
        def __init__(self, func, args=()):
            super(MyThread, self).__init__()
            self.func = func
            self.args = args

        def run(self):
            self.result = self.func(*self.args)

        def get_result(self):
            threading.Thread.join(self)
            try:
                return self.result
            except Exception:
                return None
    c = []
    for i in s:
        a = MyThread(i)
        a.start()
        a.join()
        b = a.get_result()
        c.append(b)
    c.append(keyword1)
    dic = {"yuqingzhuizong": c}
    if dic["yuqingzhuizong"][0] is None:
        return json.loads("templates/yiqing_error.json")
    else:
        return dic


# cha_xun("公司")  # 查询，传入关键字


