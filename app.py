from flask import Flask, render_template, request, jsonify
from flask_apscheduler import APScheduler
from sql_updata import sql_updata_now
from sql_read_all import SqlReadAll
from yuqingzhuizong import cha_xun
from json_updata import json_updata_now


class Config(object):
    JOBS = [
        {
            'id': 'updata',
            'func': '__main__:updata',
            'trigger': 'interval',
            'weeks': 1
        }
    ]


def updata():
    sql_updata_now()
    json_updata_now()


SqlRead = SqlReadAll()
app = Flask(__name__)
app.config.from_object(Config())  # 为实例化的flask引入配置

global keyword


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/nav.html')
def nav():
    return render_template("nav.html")


@app.route('/shouye.html')
def shouye():
    return render_template("shouye.html")


@app.route('/yuqing_genzong.html')
def yuqing_genzong():
    return render_template("yuqing_genzong.html")


@app.route('/yuqingzonglan.html')
def yuqingzonglan():
    return render_template("yuqingzonglan.html")


@app.route('/yuqingxinxi.html')
def yuqingxinxi():
    return render_template("yuqingxinxi.html")


@app.route('/search_content')
def search():
    content = request.args.get("content")
    print("搜索内容：" + content)
    global keyword
    keyword = content
    return "success"


# ========================================================json


@app.route('/keyworlds.json')
def keyworlds():
    id = request.args.get("id")
    print("是否通过搜索框访问：" + id)
    if id == "no":
        return render_template("疫情.json")
    try:  # 直接点击舆情跟踪不会触发搜索框，导致keyworld未赋值
        print("关键词：" + keyword)
        if keyword == "疫情" or keyword == "" or keyword == "舆情追踪...":
            return render_template("疫情.json")
        try:
            message = cha_xun(keyword)
            print(message)
            return jsonify(message)
        except Exception:
            return render_template("yiqing_error.json")
    except:
        return render_template("疫情.json")


@app.route('/shouye.json')
def shouye_json():
    return render_template("shouye.json")


@app.route('/wordcloud.json')
def wordcloud():
    # SqlRead.fen_ci('%')
    return render_template("wordcloud.json")


@app.route('/reci_bar.json')
def reci_bar():
    # SqlRead.words_list("%")
    return render_template("reci_bar.json")


@app.route('/wuhuMap.json')
def wuhuMap():
    return render_template("wuhuMap.json")


@app.route('/wuhuData.json')
def wuhuData():
    return render_template("wuhuData.json")


@app.route('/niandujieshou.json')
def niandujieshou():
    # SqlRead.niandujieshou()
    return render_template("niandujieshou.json")


@app.route('/rader.json')
def rader():
    # SqlRead.rader_time('%')
    return render_template("rader.json")


@app.route('/yuqingzonglan.json')
def yuqingzonglan_json():
    return render_template("yuqingzonglan.json")


# =========================================yuqingxinxi
# ==========LDA
@app.route('/LDA_2021.json', methods=['GET'])
def LDA_2021():
    return render_template("LDA_2021.json")


@app.route('/LDA_2020.json', methods=['GET'])
def LDA_2020():
    return render_template("LDA_2020.json")


@app.route('/LDA_2019.json', methods=['GET'])
def LDA_2019():
    return render_template("LDA_2019.json")


@app.route('/LDA_2018.json', methods=['GET'])
def LDA_2018():
    return render_template("LDA_2018.json")


@app.route('/LDA_2017.json', methods=['GET'])
def LDA_2017():
    return render_template("LDA_2017.json")


@app.route('/LDA_2016.json', methods=['GET'])
def LDA_2016():
    return render_template("LDA_2016.json")


@app.route('/LDA_2015.json', methods=['GET'])
def LDA_2015():
    return render_template("LDA_2015.json")


@app.route('/wordcloud_2021.json', methods=['GET'])
def wordcloud_2021_json():
    # SqlRead.fen_ci('2021%')
    return render_template("wordcloud_2021.json")


@app.route('/reci_bar_2021.json', methods=['GET'])
def reci_bar_2021():
    # SqlRead.words_list('2021%')
    return render_template("reci_bar_2021.json")


@app.route('/wordcloud_2020.json', methods=['GET'])
def wordcloud_2020_json():
    # SqlRead.fen_ci('2020%')
    return render_template("wordcloud_2020.json")


@app.route('/reci_bar_2020.json', methods=['GET'])
def reci_bar_2020():
    # SqlRead.words_list('2020%')
    return render_template("reci_bar_2020.json")


@app.route('/wordcloud_2019.json', methods=['GET'])
def wordcloud_2019_json():
    # SqlRead.fen_ci('2019%')
    return render_template("wordcloud_2019.json")


@app.route('/reci_bar_2019.json', methods=['GET'])
def reci_bar_2019():
    # SqlRead.words_list('2019%')
    return render_template("reci_bar_2019.json")


@app.route('/wordcloud_2018.json', methods=['GET'])
def wordcloud_2018_json():
    # SqlRead.fen_ci('2018%')
    return render_template("wordcloud_2018.json")


@app.route('/reci_bar_2018.json', methods=['GET'])
def reci_bar_2028():
    # SqlRead.words_list('2018%')
    return render_template("reci_bar_2018.json")


@app.route('/wordcloud_2017.json', methods=['GET'])
def wordcloud_2017_json():
    # SqlRead.fen_ci('2017%')
    return render_template("wordcloud_2017.json")


@app.route('/reci_bar_2017.json', methods=['GET'])
def reci_bar_2017():
    # SqlRead.words_list('2017%')
    return render_template("reci_bar_2017.json")


@app.route('/wordcloud_2016.json', methods=['GET'])
def wordcloud_2016_json():
    # SqlRead.fen_ci('2016%')
    return render_template("wordcloud_2016.json")


@app.route('/reci_bar_2016.json', methods=['GET'])
def reci_bar_2016():
    # SqlRead.words_list('2016%')
    return render_template("reci_bar_2016.json")


@app.route('/wordcloud_2015.json', methods=['GET'])
def wordcloud_2015_json():
    # SqlRead.fen_ci('2015%')
    return render_template("wordcloud_2015.json")


@app.route('/reci_bar_2015.json', methods=['GET'])
def reci_bar_2015():
    # SqlRead.words_list('2015%')
    return render_template("reci_bar_2015.json")


if __name__ == '__main__':
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.run(debug=True, use_reloader=False)  # host='47.119.132.9', port=8000
    # use_reloader 取消底层框架自启动，这样代码变动不会引起自动刷新
