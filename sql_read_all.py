# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年04月11日
"""
import json

import pymysql
from wordcloud import STOPWORDS
from collections import Counter
import jieba


class SqlReadAll:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = '123456'

    # ==========================================================top_6数据读取start
    def sql_top6_read(self):
        top6_list = []
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database='wuhu',
            charset='utf8'
        )
        cursor = conn.cursor()
        sql = 'select day_accept from data_broadcast;'
        try:
            cursor.execute(sql)
            row = cursor.fetchall()
            # print(list(row))
            for line in row:
                # print(line)
                top6_list.append(line[0])
            print(top6_list)
            with open("templates/top_6.json", "w", encoding="utf-8") as f:
                json.dump({"datas": top6_list}, f)
        except Exception as e:
            print('读取出错！')
            print(e)
        finally:
            cursor.close()
            conn.close()

    # =====================================================================top_6数据读取end

    # ======================================================================词云数据读取start
    def sql_wordcloud_read(self, sql_str):
        message_str = ''
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database='wuhu',
            charset='utf8'
        )
        cursor = conn.cursor()
        try:
            cursor.execute(sql_str)
            row = cursor.fetchall()
            # print(list(row))
            for line in row:
                # print(line)
                message_str += line[0]
            # print(message_str)
            return message_str
        except Exception as e:
            print('读取出错！')
            print(e)
        finally:
            cursor.close()
            conn.close()

    def wordcloud_message_read(self, sign):
        str_init1 = "select message from shizhang where year_day like '" + sign + "';"
        str_init2 = "select message from bottom_car where year_day like '" + sign + "';"
        message = self.sql_wordcloud_read(str_init1) + self.sql_wordcloud_read(str_init2)
        # print(message)
        return message

    def fen_ci(self, sign):
        message_str = self.wordcloud_message_read(sign)
        jieba_list = jieba.lcut(message_str)  # jieba.lcut分词返回一个列表
        # print(jieba_list)
        for ci in range(len(jieba_list)):  # 遍历分词后的列表元素
            if len(jieba_list[ci]) == 1:  # 如果词的个数为1即一个字的元素，用空字符串替换
                jieba_list[ci] = ''
        stopwords = set(STOPWORDS)
        stopwords.add('年月日')
        stopwords.add('没有')
        stopwords.add('我们')
        stopwords.add('现在')
        stopwords.add('这个')
        stopwords.add('一个')
        stopwords.add('就是')
        stopwords.add('rdquo')
        stopwords.add('ldquo')
        stopwords.add('hellip')
        stopwords.add('nbsp')
        stopwords.add('这样')
        stopwords.add('可以')
        stopwords.add('本人')
        stopwords.add('但是')
        stopwords.add('为什么')
        stopwords.add('已经')
        stopwords.add('他们')
        stopwords.add('市长')
        stopwords.add('你好')
        stopwords.add('小区')
        stopwords.add('不能')
        stopwords.add('一直')
        stopwords.add('如果')
        stopwords.add('领导')
        stopwords.add('因为')
        stopwords.add('办理')
        stopwords.add('尊敬')
        stopwords.add('很多')
        stopwords.add('我家')
        stopwords.add('芜湖')
        stopwords.add('芜湖市')
        stopwords.add('自己')
        stopwords.add('进行')
        stopwords.add('问题')
        stopwords.add('作为')
        stopwords.add('要求')
        stopwords.add('由于')
        stopwords.add('所以')
        stopwords.add('时间')
        stopwords.add('知道')
        stopwords.add('情况')
        stopwords.add('需要')
        stopwords.add('希望')
        stopwords.add('您好')
        stopwords.add('这些')
        stopwords.add('当时')
        stopwords.add('无法')
        stopwords.add('谢谢')
        stopwords.add('处理')
        stopwords.add('还是')
        stopwords.add('不是')
        stopwords.add('反映')
        stopwords.add('多次')
        stopwords.add('通过')
        stopwords.add('应该')
        stopwords.add('任何')
        stopwords.add('而且')
        stopwords.add('什么')
        stopwords.add('开始')
        stopwords.add('解决')
        stopwords.add('至今')
        stopwords.add('你们')
        stopwords.add('可是')
        stopwords.add('难道')
        stopwords.add('政府')
        stopwords.add('目前')
        stopwords.add('今年')
        stopwords.add('回复')
        stopwords.add('这种')
        stopwords.add('时候')
        stopwords.add('得到')
        stopwords.add('人员')
        stopwords.add('地方')
        stopwords.add('一名')
        stopwords.add('为了')
        stopwords.add('真的')
        stopwords.add('相关')
        stopwords.add('怎么')
        stopwords.add('能够')
        stopwords.add('一下')
        stopwords.add('存在')
        stopwords.add('部门')
        stopwords.add('恳请')
        stopwords.add('月份')
        stopwords.add('答复')
        stopwords.add('反应')
        stopwords.add('严重')
        stopwords.add('不了')
        stopwords.add('给予')
        stopwords.add('结果')
        stopwords.add('还有')
        stopwords.add('是否')
        stopwords.add('有关')
        stopwords.add('工作人员')
        stopwords.add('有关')
        stopwords.add('按照')
        stopwords.add('市政府')
        # print(stopwords)
        stop_path = open("./stoplist.txt", "r", encoding="utf-8")  # 导入停用词
        stop_words = stop_path.readlines()
        stop_words = [word.strip("\n") for word in stop_words]
        stopwords = stopwords | set(stop_words)
        filtered_sentence = [w for w in jieba_list if not w in stopwords]
        # filtered_sentence.remove("")
        # # print(filtered_sentence)
        counter = Counter(filtered_sentence)
        del counter[""]
        # print(dict(counter))
        list1 = counter.most_common(500)
        datas = []
        for i in list1:
            temp_dict = {'name': i[0], 'value': i[-1]}
            datas.append(temp_dict)
        # print(datas)
        if sign == "%":
            with open("templates/wordcloud.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)
        elif len(sign) > 1:
            with open("templates/wordcloud_" + sign[:4] + ".json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)

    # ======================================================================词云数据读取end

    # ======================================================================雷达图数据读取start
    def sql_time_read(self, sql_str):
        time_list = []
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database='wuhu',
            charset='utf8'
        )
        cursor = conn.cursor()
        try:
            cursor.execute(sql_str)
            row = cursor.fetchall()
            # print(list(row))
            for line in row:
                # print(line)
                time_list.append(str(line[0])[0:7])
                # print(str(line[0])[0:7])
            # print(time_list)
            return time_list
        except Exception as e:
            print('读取出错！')
            print(e)
        finally:
            cursor.close()
            conn.close()

    def time_read(self, sign):
        str_init1 = "select year_day from shizhang where year_day like '" + sign + "';"
        str_init2 = "select year_day from bottom_car where year_day like '" + sign + "';"
        list1 = self.sql_time_read(str_init1)
        # print(list1)
        list2 = self.sql_time_read(str_init2)
        # print(list2)
        time_all_list = list1 + list2
        # print(time_all_list)
        time_counter = Counter(time_all_list)
        del time_counter["NULL"]
        # print(dict(time_counter))
        return dict(time_counter)

    def rader_time(self, sign):
        day_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        if sign == "%":
            time_counter_dict = self.time_read(sign)
            print(time_counter_dict)
            legend_list = ['2015', '2016', '2017', '2018', '2019', '2020', '2021']
            time_list = []
            for year_day in time_counter_dict.keys():
                time_list.append(year_day)
            # print(time_list)
            data = []
            for year in range(2015, 2022):
                temp_dict = {}
                temp_count = []
                for day in day_list:
                    try:
                        temp_count.append(time_counter_dict[str(year) + "." + day])
                    except KeyError:
                        temp_count.append(0)
                temp_dict["value"] = temp_count
                temp_dict["name"] = str(year)
                data.append(temp_dict)
                # print(temp_dict)
            datas = {"legend": legend_list, "data": data}
            print(datas)
            with open("templates/rader.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)

        elif sign[:4] in ['2015', '2016', '2017', '2018', '2019', '2020', '2021']:
            time_counter_dict = self.time_read(sign)
            legend_list = [sign[0:4]]
            time_list = []
            for year_day in time_counter_dict.keys():
                time_list.append(year_day)
            # print(time_list)
            temp_dict = {}
            data = []
            year = sign[:4]
            temp_count = []
            for day in day_list:
                try:
                    temp_count.append(time_counter_dict[str(year) + "." + str(day)])
                except KeyError:
                    temp_count.append(0)
            temp_dict["value"] = temp_count
            temp_dict["name"] = str(year)
            data.append(temp_dict)
            # print(temp_dict)
            datas = {"legend": legend_list, "data": data}
            print(datas)
            with open("templates/rader.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)

    # ======================================================================雷达图数据读取end

    # ======================================================================饼图数据读取start
    def niandujieshou(self):
        datas = []
        pie = []
        year_list = ['2021', '2020', '2019', '2018', '2017', '2016', '2015']
        xAxis = []
        series = []
        for year in range(2015,2022):
            temp_dict = {"name": '', "value": ''}
            str1 = 'select count(*) from shizhang where year_day like "' + str(year) + '%";'
            str2 = 'select count(*) from bottom_car where year_day like "' + str(year) + '%";'
            data = self.sql_time_read(str1)[0] + self.sql_time_read(str2)[0]
            temp_dict['name'] = str(year)
            temp_dict['value'] = int(data)
            series.append(int(data))
            xAxis.append(year)
            pie.append(temp_dict)
        datas.append(pie)
        datas.append(xAxis)
        datas.append(series)
        with open("niandujieshou.json", "w", encoding="utf-8") as f:
            json.dump({"datas": datas}, f)

    # ======================================================================饼图数据读取end

    # ======================================================================热词多柱形图数据读取start
    def fen_ci_bar(self, sign):
        message_str = self.wordcloud_message_read(sign)
        jieba_list = jieba.lcut(message_str)  # jieba.lcut分词返回一个列表
        # print(jieba_list)
        for ci in range(len(jieba_list)):  # 遍历分词后的列表元素
            if len(jieba_list[ci]) == 1:  # 如果词的个数为1即一个字的元素，用空字符串替换
                jieba_list[ci] = ''
        stopwords = set(STOPWORDS)
        stopwords.add('年月日')
        stopwords.add('没有')
        stopwords.add('我们')
        stopwords.add('现在')
        stopwords.add('这个')
        stopwords.add('一个')
        stopwords.add('就是')
        stopwords.add('rdquo')
        stopwords.add('ldquo')
        stopwords.add('hellip')
        stopwords.add('nbsp')
        stopwords.add('这样')
        stopwords.add('可以')
        stopwords.add('本人')
        stopwords.add('但是')
        stopwords.add('为什么')
        stopwords.add('已经')
        stopwords.add('他们')
        stopwords.add('市长')
        stopwords.add('你好')
        stopwords.add('小区')
        stopwords.add('不能')
        stopwords.add('一直')
        stopwords.add('如果')
        stopwords.add('领导')
        stopwords.add('因为')
        stopwords.add('办理')
        stopwords.add('尊敬')
        stopwords.add('很多')
        stopwords.add('我家')
        stopwords.add('芜湖')
        stopwords.add('芜湖市')
        stopwords.add('自己')
        stopwords.add('进行')
        stopwords.add('问题')
        stopwords.add('作为')
        stopwords.add('要求')
        stopwords.add('由于')
        stopwords.add('所以')
        stopwords.add('时间')
        stopwords.add('知道')
        stopwords.add('情况')
        stopwords.add('需要')
        stopwords.add('希望')
        stopwords.add('您好')
        stopwords.add('这些')
        stopwords.add('当时')
        stopwords.add('无法')
        stopwords.add('谢谢')
        stopwords.add('处理')
        stopwords.add('还是')
        stopwords.add('不是')
        stopwords.add('反映')
        stopwords.add('多次')
        stopwords.add('通过')
        stopwords.add('应该')
        stopwords.add('任何')
        stopwords.add('而且')
        stopwords.add('什么')
        stopwords.add('开始')
        stopwords.add('解决')
        stopwords.add('至今')
        stopwords.add('你们')
        stopwords.add('可是')
        stopwords.add('难道')
        stopwords.add('政府')
        stopwords.add('目前')
        stopwords.add('今年')
        stopwords.add('回复')
        stopwords.add('这种')
        stopwords.add('时候')
        stopwords.add('得到')
        stopwords.add('人员')
        stopwords.add('地方')
        stopwords.add('一名')
        stopwords.add('为了')
        stopwords.add('真的')
        stopwords.add('相关')
        stopwords.add('怎么')
        stopwords.add('能够')
        stopwords.add('一下')
        stopwords.add('存在')
        stopwords.add('部门')
        stopwords.add('恳请')
        stopwords.add('月份')
        stopwords.add('答复')
        stopwords.add('反应')
        stopwords.add('严重')
        stopwords.add('不了')
        stopwords.add('给予')
        stopwords.add('结果')
        stopwords.add('还有')
        stopwords.add('是否')
        stopwords.add('有关')
        stopwords.add('工作人员')
        stopwords.add('有关')
        stopwords.add('按照')
        stopwords.add('市政府')
        # print(stopwords)
        stop_path = open("./stoplist.txt", "r", encoding="utf-8")  # 导入停用词
        stop_words = stop_path.readlines()
        stop_words = [word.strip("\n") for word in stop_words]
        stopwords = stopwords | set(stop_words)
        filtered_sentence = [w for w in jieba_list if not w in stopwords]
        # filtered_sentence.remove("")
        # # print(filtered_sentence)
        counter = Counter(filtered_sentence)
        del counter[""]
        # print(dict(counter))
        list1 = counter.most_common(500)
        words_dict = {}
        for i in list1:
            words_dict[i[0]] = i[-1]
        # print(words_dict)
        return words_dict

    def words_list(self, sign):
        words_dict_2015 = dict(self.fen_ci_bar("2015%"))
        words_dict_2016 = dict(self.fen_ci_bar("2016%"))
        words_dict_2017 = dict(self.fen_ci_bar("2017%"))
        words_dict_2018 = dict(self.fen_ci_bar("2018%"))
        words_dict_2019 = dict(self.fen_ci_bar("2019%"))
        words_dict_2020 = dict(self.fen_ci_bar("2020%"))
        words_dict_2021 = dict(self.fen_ci_bar("2021%"))
        keys_set = set(words_dict_2015) | set(words_dict_2016) | set(words_dict_2017) | set(words_dict_2018) | set(
            words_dict_2019) | set(words_dict_2020) | set(words_dict_2021)
        if sign == "%":
            source = [["热词", '2015', '2016', '2017', '2018', '2019', '2020', '2021']]
            for key in keys_set:
                temp_source = [key]
                try:
                    temp_source.append(words_dict_2015[key])
                except KeyError:
                    temp_source.append(0)
                try:
                    temp_source.append(words_dict_2016[key])
                except KeyError:
                    temp_source.append(0)
                try:
                    temp_source.append(words_dict_2017[key])
                except KeyError:
                    temp_source.append(0)
                try:
                    temp_source.append(words_dict_2018[key])
                except KeyError:
                    temp_source.append(0)
                try:
                    temp_source.append(words_dict_2019[key])
                except KeyError:
                    temp_source.append(0)
                try:
                    temp_source.append(words_dict_2020[key])
                except KeyError:
                    temp_source.append(0)
                try:
                    temp_source.append(words_dict_2021[key])
                except KeyError:
                    temp_source.append(0)
                source.append(temp_source)
            print(source)
            with open("templates/reci_bar.json", "w", encoding="utf-8") as f:
                json.dump({"datas": {"source": source}}, f)
        elif sign == "2021%":
            source = [["热词", '2021']]
            for key in set(words_dict_2021):
                temp_source = [key]
                try:
                    temp_source.append(words_dict_2021[key])
                except KeyError:
                    temp_source.append(0)
                source.append(temp_source)
            print(source)
            with open("templates/reci_bar_2021.json", "w", encoding="utf-8") as f:
                json.dump({"datas": {"source": source}}, f)

        elif sign == "2020%":
            source = [["热词", '2020']]
            for key in set(words_dict_2020):
                temp_source = [key]
                try:
                    temp_source.append(words_dict_2020[key])
                except KeyError:
                    temp_source.append(0)
                source.append(temp_source)
            print(source)
            with open("templates/reci_bar_2020.json", "w", encoding="utf-8") as f:
                json.dump({"datas": {"source": source}}, f)
        elif sign == "2019%":
            source = [["热词", '2019']]
            for key in set(words_dict_2019):
                temp_source = [key]
                try:
                    temp_source.append(words_dict_2019[key])
                except KeyError:
                    temp_source.append(0)
                source.append(temp_source)
            print(source)
            with open("templates/reci_bar_2019.json", "w", encoding="utf-8") as f:
                json.dump({"datas": {"source": source}}, f)

        elif sign == "2018%":
            source = [["热词", '2018']]
            for key in set(words_dict_2018):
                temp_source = [key]
                try:
                    temp_source.append(words_dict_2018[key])
                except KeyError:
                    temp_source.append(0)
                source.append(temp_source)
            print(source)
            with open("templates/reci_bar_2018.json", "w", encoding="utf-8") as f:
                json.dump({"datas": {"source": source}}, f)

        elif sign == "2017%":
            source = [["热词", '2017']]
            for key in set(words_dict_2017):
                temp_source = [key]
                try:
                    temp_source.append(words_dict_2017[key])
                except KeyError:
                    temp_source.append(0)
                source.append(temp_source)
            print(source)
            with open("templates/reci_bar_2017.json", "w", encoding="utf-8") as f:
                json.dump({"datas": {"source": source}}, f)

        elif sign == "2016%":
            source = [["热词", '2016']]
            for key in set(words_dict_2016):
                temp_source = [key]
                try:
                    temp_source.append(words_dict_2016[key])
                except KeyError:
                    temp_source.append(0)
                source.append(temp_source)
            print(source)
            with open("templates/reci_bar_2016.json", "w", encoding="utf-8") as f:
                json.dump({"datas": {"source": source}}, f)

        elif sign == "2015%":
            source = [["热词", '2015']]
            for key in set(words_dict_2015):
                temp_source = [key]
                try:
                    temp_source.append(words_dict_2015[key])
                except KeyError:
                    temp_source.append(0)
                source.append(temp_source)
            print(source)
            with open("templates/reci_bar_2015.json", "w", encoding="utf-8") as f:
                json.dump({"datas": {"source": source}}, f)

    # ======================================================================热词多柱形图数据读取end

    # ======================================================================地图图数据读取start
    def get_map_data(self):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database='wuhu',
            charset='utf8'
        )
        cursor = conn.cursor()
        sql = 'select * from map_data'
        data = []
        try:
            cursor.execute(sql)
            row = cursor.fetchall()
            for line in row:
                data_dict = {"name": "", "value": ""}
                name = line[1]
                value = line[2]
                data_dict["name"] = name
                data_dict["value"] = value
                data.append(data_dict)
            with open("templates/wuhuData.json", "w", encoding="utf-8") as f:
                json.dump({"datas": data}, f)
        except Exception as e:
            print('读取出错！')
            print(e)
        finally:
            cursor.close()
            conn.close()

    # ======================================================================地图图数据读取end

    # ======================================================================分类词云数据start
    def wordcloud_message_read_fenlei(self, year, type):
        str_init1 = "select message from shizhang where year_day like '" + year + "' and problem_type='" + type + "';"
        str_init2 = "select message from bottom_car where year_day like '" + year + "' and problem_type='" + type + "';"
        message = self.sql_wordcloud_read(str_init1) + self.sql_wordcloud_read(str_init2)
        # print(message)
        return message

    def fen_lei_ciyun(self, year, type):
        message_str = self.wordcloud_message_read_fenlei(year, type)
        jieba_list = jieba.lcut(message_str)  # jieba.lcut分词返回一个列表
        # print(jieba_list)
        for ci in range(len(jieba_list)):  # 遍历分词后的列表元素
            if len(jieba_list[ci]) == 1:  # 如果词的个数为1即一个字的元素，用空字符串替换
                jieba_list[ci] = ''
        stopwords = set(STOPWORDS)
        stopwords.add('年月日')
        stopwords.add('没有')
        stopwords.add('我们')
        stopwords.add('现在')
        stopwords.add('这个')
        stopwords.add('一个')
        stopwords.add('就是')
        stopwords.add('rdquo')
        stopwords.add('ldquo')
        stopwords.add('hellip')
        stopwords.add('nbsp')
        stopwords.add('这样')
        stopwords.add('可以')
        stopwords.add('本人')
        stopwords.add('但是')
        stopwords.add('为什么')
        stopwords.add('已经')
        stopwords.add('他们')
        stopwords.add('市长')
        stopwords.add('你好')
        stopwords.add('小区')
        stopwords.add('不能')
        stopwords.add('一直')
        stopwords.add('如果')
        stopwords.add('领导')
        stopwords.add('因为')
        stopwords.add('办理')
        stopwords.add('尊敬')
        stopwords.add('很多')
        stopwords.add('我家')
        stopwords.add('芜湖')
        stopwords.add('芜湖市')
        stopwords.add('自己')
        stopwords.add('进行')
        stopwords.add('问题')
        stopwords.add('作为')
        stopwords.add('要求')
        stopwords.add('由于')
        stopwords.add('所以')
        stopwords.add('时间')
        stopwords.add('知道')
        stopwords.add('情况')
        stopwords.add('需要')
        stopwords.add('希望')
        stopwords.add('您好')
        stopwords.add('这些')
        stopwords.add('当时')
        stopwords.add('无法')
        stopwords.add('谢谢')
        stopwords.add('处理')
        stopwords.add('还是')
        stopwords.add('不是')
        stopwords.add('反映')
        stopwords.add('多次')
        stopwords.add('通过')
        stopwords.add('应该')
        stopwords.add('任何')
        stopwords.add('而且')
        stopwords.add('什么')
        stopwords.add('开始')
        stopwords.add('解决')
        stopwords.add('至今')
        stopwords.add('你们')
        stopwords.add('可是')
        stopwords.add('难道')
        stopwords.add('政府')
        stopwords.add('目前')
        stopwords.add('今年')
        stopwords.add('回复')
        stopwords.add('这种')
        stopwords.add('时候')
        stopwords.add('得到')
        stopwords.add('人员')
        stopwords.add('地方')
        stopwords.add('一名')
        stopwords.add('为了')
        stopwords.add('真的')
        stopwords.add('相关')
        stopwords.add('怎么')
        stopwords.add('能够')
        stopwords.add('一下')
        stopwords.add('存在')
        stopwords.add('部门')
        stopwords.add('恳请')
        stopwords.add('月份')
        stopwords.add('答复')
        stopwords.add('反应')
        stopwords.add('严重')
        stopwords.add('不了')
        stopwords.add('给予')
        stopwords.add('结果')
        stopwords.add('还有')
        stopwords.add('是否')
        stopwords.add('有关')
        stopwords.add('工作人员')
        stopwords.add('有关')
        stopwords.add('按照')
        stopwords.add('市政府')
        # print(stopwords)
        stop_path = open("./stoplist.txt", "r", encoding="utf-8")  # 导入停用词
        stop_words = stop_path.readlines()
        stop_words = [word.strip("\n") for word in stop_words]
        stopwords = stopwords | set(stop_words)
        filtered_sentence = [w for w in jieba_list if not w in stopwords]
        # filtered_sentence.remove("")
        # # print(filtered_sentence)
        counter = Counter(filtered_sentence)
        del counter[""]
        # print(dict(counter))
        list1 = counter.most_common(500)
        datas = []
        for i in list1:
            temp_dict = {'name': i[0], 'value': i[-1]}
            datas.append(temp_dict)
        if len(datas) == 0:
            datas.append({'name': "暂无相关", 'value': 1})
            datas.append({'name': "热词数据", 'value': 1})

        print(datas)

        if type == "我要咨询":
            with open("templates/wordcloud_" + year[:4] + "_zixun.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)
        elif type == "我要投诉":
            with open("templates/wordcloud_" + year[:4] + "_tousu.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)
        elif type == "我要求助":
            with open("templates/wordcloud_" + year[:4] + "_qiuzhu.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)
        elif type == "我要举报":
            with open("templates/wordcloud_" + year[:4] + "_jubao.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)
        elif type == "我要建议":
            with open("templates/wordcloud_" + year[:4] + "_jianyi.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)
        elif type == "其他":
            with open("templates/wordcloud_" + year[:4] + "_qita.json", "w", encoding="utf-8") as f:
                json.dump({"datas": datas}, f)

    def fen_lei_ciyun_run(self, sign):
        self.fen_lei_ciyun(sign, "我要咨询")
        self.fen_lei_ciyun(sign, "我要建议")
        self.fen_lei_ciyun(sign, "我要举报")
        self.fen_lei_ciyun(sign, "我要投诉")
        self.fen_lei_ciyun(sign, "我要求助")
        self.fen_lei_ciyun(sign, "其他")
# ======================================================================分类词云数据end
