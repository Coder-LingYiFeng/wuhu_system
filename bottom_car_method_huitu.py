import pandas as pd
import pymysql
import pyecharts.options as opts
from pyecharts.charts import Pie


def bottom_car_method():
    conn = pymysql.connect(host="localhost", port=3306, user="root",
                           password="123456", database="wuhu", charset="utf8")
    sql = "select * from bottom_car;"
    # dataframe对齐
    # pd.set_option("display.unicode.ambiguous_as_wide",True)
    # pd.set_option("display.unicode.east_asian_width",True)
    df = pd.read_sql(sql, conn)
    sql1 = "select * from shizhang;"
    df1 = pd.read_sql(sql1, conn)
    df = pd.concat([df, df1], axis=0)

    # 方法比例图
    # 玫瑰图
    data = df.groupby("method").size()
    data = data.drop("NULL")
    data = data.sort_values()
    data_pair = [list(z) for z in zip(data.index, data.values.tolist())]
    (
        Pie(init_opts=opts.InitOpts(width='570px', height='360px'))
            .add(series_name='', data_pair=data_pair, radius=["40%", "90%"], center=["50%", "50%"], rosetype="area"
                 , label_opts=opts.LabelOpts(is_show=False))
            .set_colors(["#5470C6", "#9FE080", "#FFDC60", "#EE6666", "#7ED3F4", "#3BA272", "#FF915A", "#006EA5"])
            .set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_left="90%",
                                                         orient="vertical", is_show=False))   # is_show图例不展示
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    ).render("templates/method.html")
    print("方法比例图绘制完成！")


