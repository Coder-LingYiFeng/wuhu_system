import pandas as pd
import pymysql
import pyecharts.options as opts
from pyecharts.charts import Line


def bottom_car_problem_type():
    conn = pymysql.connect(host="localhost", port=3306, user="root",
                           password="123456", database="wuhu", charset="utf8")
    sql = "select * from bottom_car;"
    # dataframe对齐
    # pd.set_option("display.unicode.ambiguous_as_wide",True)
    # pd.set_option("display.unicode.east_asian_width",True)
    df = pd.read_sql(sql, conn)

    # 历年问题种类统计图
    def suojian(s):
        s = s.split(".")[0]
        return s

    df["year_day"] = df["year_day"].map(suojian)
    fenlei_2 = df.groupby(["year_day", "problem_type"]).size().unstack()
    (
        Line(init_opts=opts.InitOpts(width='1200px', height='500px'))
            .add_xaxis(['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021'])
            .add_yaxis("其他", fenlei_2["其他"], is_connect_nones=True, symbol_size=4)
            .add_yaxis("我要举报", fenlei_2["我要举报"], is_connect_nones=True, symbol_size=4)
            .add_yaxis("我要咨询", fenlei_2["我要咨询"], is_connect_nones=True, symbol_size=4)
            .add_yaxis("我要建议", fenlei_2["我要建议"], is_connect_nones=True, symbol_size=4)
            .add_yaxis("我要投诉", fenlei_2["我要投诉"], is_connect_nones=True, symbol_size=4)
            .add_yaxis("我要求助", fenlei_2["我要求助"], is_connect_nones=True, symbol_size=4)
            .set_global_opts(title_opts=opts.TitleOpts(title="历年问题种类图"),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, orient='horizontal'))
    ).render("templates/problem_type.html")
    print("问题种类图绘制完成！")

