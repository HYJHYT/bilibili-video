# -*- coding: UTF-8 -*- #

import sqlite3
import pandas as pd

# 连接数据库
from sqlalchemy import create_engine


def get_conn():
    conn = sqlite3.connect('bilibili.sqlite')

    # 创建游标：
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):  # 关闭数据库
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):  # sql语句查询
    '''
    :param sql:
    :param args:
    :return:返回结果，((),())形式
    '''
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()  # 获取结果
    close_conn(conn, cursor)
    return res

def save(sql, *args):  #sql语句保存
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    conn.commit()
    close_conn(conn, cursor)

#查询各表范围值
def search_between(database):
    sql = "select * from %s where id=1"%database
    res = query(sql)
    min = fetcher(res, 1)
    max = fetcher(res, 2)
    print(min,max)
    min = 200 if not min else min[0]
    max = 1600000 if not max else max[0]
    return min,max


# 对查询数据进行处理
def fetcher(list_of_tups, ind):
    return [x[ind] for x in list_of_tups]

#图四查询数据库
def find_echarts1():
    min,max = search_between('echart1')
    sql = 'select "UP主","硬币数" from BData where "硬币数" between ? and ? order by "硬币数" desc limit 9'
    res = query(sql,min,max)
    data1 = fetcher(res, 0)
    data2 = fetcher(res, 1)
    data3 = [int(i / 500000 * 100) for i in data2]
    return data1, data2, data3

#图三查询数据库
def find_echarts2():
    min, max = search_between('echart2')
    sql = 'select "UP主","关注数" from BData where "关注数" between ? and ? order by "关注数" desc limit 9'
    res = query(sql,min,max)
    data1 = fetcher(res, 0)
    data2 = fetcher(res, 1)
    return data1, data2

#图一查询数据库
def find_echarts3():
    #从表3中取出要显示的字段
    sql0 = "select * from echart3"
    res0 = query(sql0)
    if res0:
        words = res0[0][1:]
    else:
        words = ["播放量", "收藏数", "点赞数", "弹幕数", "评论数", "分享数"]
    sql = 'select "id",%s,%s,%s,%s,%s,%s from BData order by "发布时间" limit 4'%words
    res = query(sql)
    data = [fetcher(res, i) for i in range(7)]
    return data, words

#图二查询数据库
def find_echarts4():
    min, max = search_between('echart4')
    words = ("id", "收藏数", "点赞数", "分享数")
    sql = 'select %s,%s,%s,%s from BData  where "播放量" between ? and ?  order by "播放量"  desc limit 9' % words
    res = query(sql,min, max)
    data = [fetcher(res, i) for i in range(4)]
    return data, words

#图五查询数据库
def find_echarts5():
    sql0 = "select * from echart5"
    res0 = query(sql0)
    if res0:
        words = res0[0][1:]
    else:
        words = ("收藏数", "分享数")
    sql = 'select %s,%s,%s from BData order by length("视频名字") limit 4' % ("id",*words)
    res = query(sql)
    data = [fetcher(res, i) for i in range(3)]
    return data, words

#图表格查询数据库
def find_table():
    words = ["视频id","发布时间","关注数","播放量"]
    sql = 'select id,"发布时间","关注数","播放量" from BData order by "播放量" desc limit 4 '
    res = query(sql)
    return res,words

#图六查询数据库
def find_echarts6():
    min, max = search_between('echart6')
    sql = 'select id,"弹幕数" from BData where "弹幕数" between ? and ?  order by "弹幕数" desc limit 4'
    res = query(sql,min, max)
    data = [{"name":"视频id"+str(i[0]),'value':i[1]} for i in res]
    sum = 0
    for i in res:
        sum +=i[1]
    return data,sum

def creat_table():
    sql = "create table echart4(id INTEGER primary key AUTOINCREMENT , watchmin int,watchmax int )"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    close_conn(conn, cursor)

#保存图表1的参数
def save_echart(min,max,table,columin,columax):
    sql = "update %s set %s=?,%s=? "%(table,columin,columax)
    save(sql,min,max)

#保存图表三关键字
def save_echart3(form):
    columns = tuple(form.keys())
    values = list(form.values())

    sql = "update echart3 set %s=?,%s=?,%s=?,%s=?,%s=?,%s=? "%columns
    save(sql, *values)

def save_echart5(form):
    columns = tuple(form.keys())
    values = list(form.values())
    sql = "update echart5 set %s=?,%s=?"%columns
    save(sql, *values)

#保存注册账号
def save_admin(user,password):
    sql ="insert into admin values(null,?,?)"
    save(sql,user, password)

#查询账号
def check_admin(user):
    sql = "select password from admin where user=?"
    res = query(sql,user)
    if res:
        return res[0]
    return False




if __name__ == '__main__':
    # 存入数据
    # engine = create_engine('sqlite:///bilibili.sqlite')
    # conn = engine.connect()
    # data = pd.read_csv('BData.csv',encoding = 'gbk')
    # print(data)
    # find_echarts1()
    # print(search_between('echart2'))
    # creat_table()
    # search_between('echart4')
    # print(find_echarts3())
    # sql0 = "select * from echart3"
    # res0 = query(sql0)
    # print(res0)
    # save_echart(220, 16000000,'echart6','barragemin','barragemax')
    # save_admin("britney", "britney994711")
    # data.to_sql(name="BData", con=conn, if_exists="replace",index=False)
    params = {
        'keyword1': '播放量',
        'keyword2': '收藏数',

    }
    save_echart5(params)