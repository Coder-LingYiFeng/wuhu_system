# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年01月29日
"""
from get_shizhang import modular_two
from data_broadcast import modular_three
from bottom_car import modular_four
from sql_create_wuhu import ready
from sql_map_data import sql_map_data_run


def sql_updata_now():
    ready()
    modular_two()
    modular_three()
    modular_four()
    sql_map_data_run()


# sql_update_now()

