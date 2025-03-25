import codecs
import csv
import json
import math
import numpy as np
import os
import pandas as pd
import re
import requests
import schedule
import sqlalchemy
import time
from collections import Counter
from lxml import etree
from selenium import webdriver
from sqlalchemy import create_engine

Furl = 'https://www.bilibili.com/v/popular/rank/all'
drive = webdriver.Chrome()
drive.get(Furl)  # 获取网页源码
dom = etree.HTML(drive.page_source, etree.HTMLParser(encoding='utf-8'))  # 源码解析
cookies = {}
cookie_str = 'innersign=0; buvid3=9A5B53FA-6836-2CD6-B40D-6133C33FB9BD28227infoc; b_nut=1667205028; ' \
             'b_lsid=631031753_1842D29D0F3; _uuid=22DA581F-13D1-EABE-C952-29810ECE29106326045infoc; ' \
             'buvid_fp=9a9571e579f7626b56e48550f6df7de2; ' \
             'buvid4=31A17420-C156-80AC-3F20-5EB8C26B41D929829-022103116-eIfWn4gMTvHDKVJPNTc2ig== '
for i in cookie_str.split(';'):  # 整理cookie
    k, v = i.split('=', 1)
    cookies[k] = v
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.127 Safari/537.36'}
# 1111

def GetBilibiliData(dom=None, cookies=None, header=None):
    """

    :param dom:
    :param cookies:
    :param header:
    :return: 返回一个B站数据列表，元素顺序为：BData，Tag
    """
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' B,start')
    VideoName = dom.xpath('//div[@class="rank-container"]//div[@class="info"]/a/text()')  # 视频名字

    UPName = dom.xpath(
        '//div[@class="rank-container"]//div[@class="info"]//span[@class="data-box up-name"]/text()')  # up主名字
    UPName = [x.strip() for x in UPName]

    VideoUrl = dom.xpath('//div[@class="rank-container"]//div[@class="img"]//a/@href')  # 视频链接
    VideoUrl = ['https:' + str(x) for x in VideoUrl]

    Pudate = []  # 发布时间
    biaoqian = []  # Tag
    for i in VideoUrl:
        web_data = requests.get(i, cookies=cookies, headers=header)
        dom_web = etree.HTML(web_data.text)
        date = dom_web.xpath('//div[@class="left-container"]//span[@class="pudate-text"]/text()')
        date = [x.strip() for x in date]
        Tag = dom_web.xpath('//div[@id="v_tag"]//li[@class="tag"]/div/a/text()')
        Tag = [x.strip() for x in Tag]
        biaoqian.append(Tag)
        if date:
            Pudate.append(date[0])
        elif not date:
            Pudate.append('')
        time.sleep(1)

    vmid = []  # up主id
    follower = []  # 关注数
    UPUrl = dom.xpath('//div[@class="rank-container"]//div[@class="info"]//div[@class="detail"]/a/@href')  # up链接
    for x in UPUrl:
        vmid.append(x.split('/')[3])
    for x in vmid:
        JsonText = requests.get('https://api.bilibili.com/x/relation/stat?vmid=' + x + '&jsonp=jsonp', cookies=cookies,
                                headers=header)
        follower.append(json.loads(JsonText.text)['data']['follower'])
        time.sleep(1)

    BV = []  # BV号
    AV = []  # AV号
    coin = []  # 硬币数
    danmaku = []  # 弹幕数
    favorite = []  # 收藏数
    like = []  # 点赞数
    reply = []  # 评论数
    share = []  # 分享数
    view = []  # 播放量
    cid = []  # 弹幕id
    for x in VideoUrl:
        BV.append(x.split('/')[4])
    for x in range(len(BV)):
        AV.append(BvToAv(BV[x]))
    for x in AV:
        JsonText = requests.get('https://api.bilibili.com/x/web-interface/view?aid=' + str(x), cookies=cookies,
                                headers=header)
        coin.append(json.loads(JsonText.text)['data']['stat']['coin'])  # 硬币
        view.append(json.loads(JsonText.text)['data']['stat']['view'])  # 播放量
        danmaku.append(json.loads(JsonText.text)['data']['stat']['danmaku'])  # 弹幕数
        favorite.append(json.loads(JsonText.text)['data']['stat']['favorite'])  # 收藏数
        like.append(json.loads(JsonText.text)['data']['stat']['like'])  # 点赞数
        reply.append(json.loads(JsonText.text)['data']['stat']['reply'])  # 评论数
        share.append(json.loads(JsonText.text)['data']['stat']['share'])  # 分享数
        cid.append(json.loads(JsonText.text)['data']['cid'])  # 弹幕id
        time.sleep(1)

    BData = pd.DataFrame({
        '视频名字': VideoName,
        'UP主': UPName,
        '视频链接': VideoUrl,
        '发布时间': Pudate,
        '关注数': follower,
        '硬币数': coin,
        '播放量': view,
        '弹幕数': danmaku,
        '收藏数': favorite,
        '点赞数': like,
        '评论数': reply,
        '分享数': share,
        # 'cid': cid,
    })
    Tags = pd.DataFrame({"Tag": biaoqian})
    # 去掉空白值
    BData = BData.dropna()
    Tags = Tags.dropna()

    result = [BData, Tags]

    # 创建数据库连接
    engine = create_engine('sqlite:///bilibili.sqlite')
    conn = engine.connect()
    BData.to_csv('BData.csv')
    # 存入数据库
    BData.to_sql(name="BData", con=conn, if_exists="replace", index=False)
    Tags.to_csv('Tag.csv')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' B，ok')
    return result


def GetDanMu(cid=None):
    """
    获取弹幕数据
    :param cid:每个视频的弹幕id，请输入列表形式
    :return: 以列表的形式返回总弹幕数据，每个元素以DataFrame存储每个视频的弹幕
    """
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' 弹幕获取开始')
    cookies = {}
    cookie_str = "buvid3=786AB314-DD8B-084F-D4F5-F4390F2F4A7948593infoc; " \
                 "_uuid=219A51710-9572-EA69-EDB9-82EC3C9D7310670342infoc; " \
                 "buvid4=9E7341D6-2410-76F6-7388-D7F35C9236D792155-022070110-eIfWn4gMTvHDKVJPNTc2ig==; " \
                 "buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; blackside_state=0; LIVE_BUVID=AUTO1816567712134523; " \
                 "nostalgia_conf=-1; hit-dyn-v2=1; b_nut=100; b_ut=5; sid=67xxrd6u; " \
                 "fingerprint3=48233d61a00e778d123f75cdbb22f628; DedeUserID=33380965; " \
                 "DedeUserID__ckMd5=2185d1e4132c6d43; SESSDATA=d99f0d2a,1682945219,12b1c*b1; " \
                 "bili_jct=53ca4fd87b67c0c722a6a32d6a3ad801; hit-new-style-dyn=0; CURRENT_FNVAL=4048; " \
                 "is-2022-channel=1; i-wanna-go-back=-1; rpdid=|(JY)k)kl~YR0J'uYY)l~kY~~; CURRENT_QUALITY=116; " \
                 "fingerprint=092e582cc92e4f4cb23da6e4ceface7f; bp_article_offset_33380965=732833420731744300; " \
                 "buvid_fp=d7ed432cd3012aeb1a1791ed7e3d8bdb; PVID=1; bp_video_offset_33380965=734194805124366500; " \
                 "b_lsid=5BC45942_184C70CB2FF; innersign=1 "
    for i in cookie_str.split(';'):  # 整理cookie
        k, v = i.split('=', 1)
        cookies[k] = v
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/100.0.4896.127 Safari/537.36'}
    r = 0
    for c in cid:
        danmu_data = requests.get('https://comment.bilibili.com/' + str(c) + '.xml', cookies=cookies,
                                  headers=header)
        danmu_data.encoding = danmu_data.apparent_encoding
        dt = danmu_data.text
        danmu_web = etree.HTML(dt.encode('utf-8'))
        danmu = danmu_web.xpath('//d/text()')
        date = []
        d = []
        for x in danmu_web.xpath('//d/@p'):
            d.append(x.split(',')[4])
        for xy in d:
            xy = time.strftime("%Y/%m/%d %H:%M", time.gmtime(int(xy)))
            date.append(xy)
        dm = pd.DataFrame({
            '弹幕发布时间': date,
            '弹幕内容': danmu
        })
        if os.path.exists('danmu'):
            dm.to_csv('danmu/' + str(r) + '.csv')
            r += 1
        else:
            os.mkdir('danmu')
            dm.to_csv('danmu/' + str(r) + '.csv')
            r += 1
        time.sleep(1)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' 弹幕获取完成')


def BvToAv(Bv):
    # 1.去除Bv号前的"Bv"字符
    BvNo1 = Bv[2:]
    keys = {
        '1': '13', '2': '12', '3': '46', '4': '31', '5': '43', '6': '18', '7': '40', '8': '28', '9': '5',
        'A': '54', 'B': '20', 'C': '15', 'D': '8', 'E': '39', 'F': '57', 'G': '45', 'H': '36', 'J': '38', 'K': '51',
        'L': '42', 'M': '49', 'N': '52', 'P': '53', 'Q': '7', 'R': '4', 'S': '9', 'T': '50', 'U': '10', 'V': '44',
        'W': '34', 'X': '6', 'Y': '25', 'Z': '1',
        'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41',
        'k': '16', 'm': '11', 'n': '37', 'o': '2',
        'p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48', 'v': '23', 'w': '55', 'x': '32', 'y': '14',
        'z': '19'

    }
    # 2. 将key对应的value存入一个列表
    BvNo2 = []
    for index, ch in enumerate(BvNo1):
        BvNo2.append(int(str(keys[ch])))

    # 3. 对列表中不同位置的数进行*58的x次方的操作

    BvNo2[0] = int(BvNo2[0] * math.pow(58, 6))
    BvNo2[1] = int(BvNo2[1] * math.pow(58, 2))
    BvNo2[2] = int(BvNo2[2] * math.pow(58, 4))
    BvNo2[3] = int(BvNo2[3] * math.pow(58, 8))
    BvNo2[4] = int(BvNo2[4] * math.pow(58, 5))
    BvNo2[5] = int(BvNo2[5] * math.pow(58, 9))
    BvNo2[6] = int(BvNo2[6] * math.pow(58, 3))
    BvNo2[7] = int(BvNo2[7] * math.pow(58, 7))
    BvNo2[8] = int(BvNo2[8] * math.pow(58, 1))
    BvNo2[9] = int(BvNo2[9] * math.pow(58, 0))

    # 4.求出这10个数的合
    sum = 0
    for i in BvNo2:
        sum += i
    # 5. 将和减去100618342136696320
    sum -= 100618342136696320
    # 6. 将sum 与177451812进行异或
    temp = 177451812

    return sum ^ temp


def TopX(data=None, x=10, index=None, ascending=False, *z):
    """
    获取前几的方法
    :param data: 数据来源
    :param x: 前x个
    :param index: 按index进行排序
    :param ascending: 升序还是降序，默认降序
    :param z: 最后显示z部分
    :return:按index排序的结果
    """
    try:
        top = data.sort_values(by=index, ascending=ascending)[:x]
        result = top.loc[:, z]
        return result
    except:
        print("请检查参数是否正确")


def TagTop(data, x):
    """
    统计Tag前几的方法
    :param x: 前x个
    :param data: 数据源
    :return:结果
    """
    t = []
    for x in data['Tag']:
        for y in x.split(','):
            t.append(y)
    number = Counter(t)
    # 使用most_common()函数
    result = number.most_common()
    return result[:x]


def AccordingToString(data=None, x=10, ascending=False, index=None, *z):
    """
    根据字符串长度来排序
    :param data:数据源
    :param x: 前几个
    :param ascending:排序方式，默认降序
    :param index: 根据index排序
    :param z:显示z部分
    :return:返回处理结果
    """
    l = [len(x) for x in data[index]]
    data[index] = l
    result = TopX(data=data, x=x, index=index, ascending=ascending, z=z)
    return result


if __name__ == '__main__':
    # schedule.every().day.at("02:33").do(GetBilibiliData, dom=dom, cookies=cookies, header=header)
    # # schedule.every().day.at("02:39").do(GetDanMu, cid=np.array(pd.read_csv('BData.csv')['cid']).tolist())
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    GetBilibiliData( dom = dom, cookies = cookies, header = header)
