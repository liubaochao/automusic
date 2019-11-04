#-*- coding: UTF-8 -*-
import urllib2
import urllib
import cookielib
import json
import requests
import time
import os.path

import sys

url_login = "https://login.xiami.com/member/login"
AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
headers = {'User-Agent': AGENT}
# 该模块主要功能是提供可存储cookie的对象。使用此模块捕获cookie并在后续连接请求时重新发送，还可以用来处理包含cookie数据的文件
cj = cookielib.CookieJar()
url_recommend = "http://www.xiami.com/song/playlist/id/1/type/9/cat/json"
url_mess = 'http://www.xiami.com/song/playlist/id/%s/type/0/cat/json'
local_download_path = ''
email = ''
password = ''


def init():
    global email, password, local_download_path
    print "init"
    f = open("account")
    email = f.readline().strip()
    password = f.readline().strip()
    local_download_path = f.readline()

    # build_opener([handler1[handler2, ...]])
    # 参数handler是Handler实例，常用的有HTTPBasicAuthHandler、HTTPCookieProcessor、ProxyHandler等。
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # 安装不同的opener对象作为urlopen()使用的全局opener。
    urllib2.install_opener(opener)

    #获取当前时间
    currentDay = time.strftime("%Y-%m-%d", time.localtime())
    local_download_path = local_download_path + currentDay + '/'
    print 'create dir:', local_download_path
    if os.path.isdir(local_download_path):
        pass
    else:
        os.makedirs(local_download_path)


def login():
    print "start login"
    form = {'email': email, 'password': password, 'submit': 'log-in'}
    # 这个函数只能接收key - value pair格式的数据。即只针对dict的, 并且目前不提供urldecode方法
    # eg:{'spam': 1, 'eggs': 2, 'bacon': 0} --> 'eggs=2&bacon=0&spam=1'
    form_encode = urllib.urlencode(form)
    headers['Referer'] = url_login
    request = urllib2.Request(url_login, form_encode, headers) #headers说明如何添加头到你的HTTP请求
    response = urllib2.urlopen(request)
    for cookie in enumerate(cj):
        print '--------cookie-----------'
        print cookie[1].name, urllib.unquote(cookie[1].value)
        print '--------cookie-----------'


def getRecommend():
    print 'getRecommend'
    headers['Referer'] = url_recommend
    request = urllib2.Request(url_recommend, headers=headers)
    response = urllib2.urlopen(request)
    return response.read()


def decode_xiami_link(mess):
    """decode xm song link"""
    rows = int(mess[0])
    url = mess[1:]
    len_url = len(url)
    cols = len_url / rows
    re_col = len_url % rows  # how many rows need to extend 1 col for the remainder

    #     for row in range(rows+1):
    #         print url[row*(cols+1):row*(cols+1)+cols+1]

    l = []
    for row in xrange(rows):
        ln = cols + 1 if row < re_col else cols
        l.append(url[:ln])
        url = url[ln:]

    durl = ''
    for i in xrange(len_url):
        durl += l[i % rows][i / rows]

    return urllib.unquote(durl).replace('^', '0')


def parseSongs(jsonStr):
    #     print 'parse songs', jsonStr
    # json模块提供了一种很简单的方式来编码和解码JSON数据。 其中两个主要的函数是json.dumps()和json.loads()
    songs = json.loads(jsonStr)

    #为了解决UnicodeEncodeError: ‘ascii’ codec can’t encode异常错误
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # print "---------1-------"
    # with open('json.txt', "wb") as f:
    #     f.write(json.dumps(songs, indent=4, sort_keys=False, ensure_ascii=False))
    # print "---------1-------"

    print type(songs['data']['trackList'])
    for song in songs['data']['trackList']:
        song_info_url = url_mess % song['songId']
        # print song_info_url
        request = urllib2.Request(song_info_url, headers=headers)
        response = urllib2.urlopen(request)
        result = response.read()
        songInfo = json.loads(result)
        songname = songInfo['data']['trackList'][0]['songName']
        download_url = decode_xiami_link(songInfo['data']['trackList'][0]['location'])

        # print '-------------json-------------'
        # print (json.dumps(songInfo, indent=4, sort_keys=False, ensure_ascii=False))
        # print '-------------json-------------'

        print'------------------------------------------------------------------------------------------------------------------------'
        print songname
        print download_url
        print'------------------------------------------------------------------------------------------------------------------------'
        download(songname, download_url)


# download_with_timeout(songname, download_url, 60)


def download(songname, url):
    songname = songname.replace(u"/", " ")
    localfile = local_download_path + songname + ".mp3"
    if os.path.exists(localfile):
        print localfile, " has exists !!!"
    else:
        print "download ", songname, ' from ', url, ' to ', localfile
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = response.read()
        with open(localfile, "wb") as code:
            code.write(data)




if __name__ == '__main__':
    print "auto download daily music"
    init()
    login()
    jsonStr = getRecommend()
    parseSongs(jsonStr)
















