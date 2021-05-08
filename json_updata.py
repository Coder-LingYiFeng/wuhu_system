# -*-coding:utf-8-*-
"""
作者：LYF
日期：2021年05月07日
"""
from sql_read_all import SqlReadAll

SqlRead = SqlReadAll()


def json_updata_now():
    SqlRead.fen_ci('%')
    SqlRead.words_list("%")
    SqlRead.niandujieshou()
    SqlRead.rader_time('%')
    SqlRead.fen_ci('2021%')
    SqlRead.words_list('2021%')
    SqlRead.fen_ci('2020%')
    SqlRead.words_list('2020%')
    SqlRead.fen_ci('2019%')
    SqlRead.words_list('2019%')
    SqlRead.fen_ci('2018%')
    SqlRead.words_list('2018%')
    SqlRead.fen_ci('2017%')
    SqlRead.words_list('2017%')
    SqlRead.fen_ci('2016%')
    SqlRead.words_list('2016%')
    SqlRead.fen_ci('2015%')
    SqlRead.words_list('2015%')
