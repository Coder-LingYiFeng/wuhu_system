# -*-coding:utf-8-*-
"""
作者：LYF
日期：2020年12月04日
"""
from pyecharts.charts import Line, Bar, Page
from pyecharts import options as opts
from collections import Counter
from sql_time_read import *


def xinjian_time_huitu():
    xaxis = []
    yaxis = []
    end = get_id_max()
    f_data = []
    for i in range(1, end):
        data = sql_read(f'select year_day from shizhang where id = {i}')
        f_data.append(data)
    # print(f_data)
    counter = dict(Counter(f_data))  # 统计词频
    # print(counter)
    for key, value in counter.items():
        xaxis.append(key)
        yaxis.append(value)
    # print(xaxis)
    # print(yaxis)
    line = (
        Line(init_opts=opts.InitOpts(width='1200px', height='500px'))
        .add_xaxis(xaxis)
        .add_yaxis('单位：封', yaxis)
        .set_colors('#9370DB')
        .set_global_opts(title_opts={'text': '每月邮件折线图'})
        .set_global_opts(xaxis_opts=(opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90), name='时间')),
                         yaxis_opts=opts.AxisOpts(name='单位/封'))
    )
    bar = (
        Bar(init_opts=opts.InitOpts(width='1200px', height='400px'))
        .add_xaxis(xaxis)
        .add_yaxis('单位：封', yaxis)
        .set_global_opts(title_opts={'text': '每月邮件柱形图'})
        .set_global_opts(xaxis_opts=(opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90), name='时间')),
                         yaxis_opts=(opts.AxisOpts(name='单位/封')),
                         datazoom_opts=opts.DataZoomOpts(range_start=10, range_end=50)  # 设置x轴可拖动
                         )
    )

    page = (
        Page()
        .add(line)
        .add(bar)
    )
    page.render('templates/每月邮件折线-柱形图合页.html')
