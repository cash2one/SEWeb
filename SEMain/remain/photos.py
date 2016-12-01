# coding:utf-8

import requests
import sys
import re
import time,datetime
import threading
import json
from urllib import urlencode

reload(sys)
sys.setdefaultencoding("utf8")

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)

# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

#page=0 开始
def baiduPhoto(word,page):
    global mutex
    baiduRes=[]
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord="+word+"&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word="+word+"&face=0&istype=2nc=1&pn="+str(page*30)+"&rn=30"
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get img url from baidu failed"
        return
    result = response.content.decode('utf-8')
    # print result
    imgurls = resolveImgUrl(result)
    for url in imgurls:
        baiduRes.append(url)

    mutex.acquire()
    myans['baidu']=baiduRes
    mutex.release()

def sogouPhoto(word,page):
    global mutex
    sogouRes=[]
    url = "http://pic.sogou.com/pics?query="+str(word)+"&start="+str(page*48)
    try:
        response=requests.get(url,timeout=2)
        # print response.text
        pattern = "imgTempData={\"(.*?)};"

        result = response.content.decode('utf-8')
        matchObj = re.search(pattern,result,re.M)
        if matchObj:
            # print "Yes===>"
            content = matchObj.group(1)
            pattern = "\"pic_url\":\"(.*?)\""
            matchObj = re.findall(pattern,content.__str__(),re.M)
            for item in matchObj:
                sogouRes.append(item)
            mutex.acquire()
            myans['sogou']=sogouRes
            mutex.release()
        else:
            print "get total failed from sogou"
    except:
        print "get img url from sogou failed"
        return

def so360Photo(word,page):
    global mutex
    so360Res=[]
    url="http://image.so.com/j?q="+word+"&src=srp&sn="+str(page*30)+"&pn=30"
    try:
        response=requests.get(url,timeout=2)
    except:
        print "get img url from 360 failed"
        return
    result=response.text.encode('ISO-8859-1').decode('utf-8')
    pattern = "\"img\":\"(.*?)\""
    matchObj = re.findall(pattern,result,re.M)
    if matchObj:
        for item in matchObj:
            so360Res.append(item.replace("\\",""))
        mutex.acquire()
        myans['s360']=so360Res
        mutex.release()

def chinaSoPhoto(word,page):
    global mutex
    chinaRes=[]
    url="http://image.chinaso.com/getpic?rn=72&st="+str(page*72)+"&q="+word+"&t="+str(time.mktime(datetime.datetime.now().timetuple()))
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get img from chinaso failed"
        return
    result=response.text
    # print result
    pattern = "\"url\":\"(.*?)\""
    matchObj = re.findall(pattern,result,re.M)
    if matchObj:
        for item in matchObj:
            chinaRes.append(item.replace("\\",""))
        mutex.acquire()
        myans['chinaSo']=chinaRes
        mutex.release()

def getBingCVID():
    url = "http://cn.bing.com/"
    try:
        response = requests.get(url,timeout=1)
        html_text = response.text
        try:
            m= re.search("IG:\"(.*)\",EventID:",html_text)
            if m:
                IG= m.group(1)
                print "cvid="+IG
                return IG
        except Exception as e:
            print(e)

    except:
        print "Get Bing cvid error"
    return None

def bingPhoto(word,page):
    IG=getBingCVID()
    global mutex
    bingRes=[]
    url="http://cn.bing.com/images/async?q="+word+"&async=content&first="+str(1+page*35)+"&count=35&IG="+IG
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get img from bing failed"
        return
    result = response.text
    pattern = "src2=\"(.*?)\""
    matchObj = re.findall(pattern,result,re.M)
    if matchObj:
        for item in matchObj:
            bingRes.append(item.replace("amp;",""))
        mutex.acquire()
        myans['bing']=bingRes
        mutex.release()

def start(word,page,search_dict):
    global myans,mutex
    mutex = threading.Lock()
    threads=[]
    myans={}

    if(search_dict['bing']=='true'):
        threads.append(threading.Thread(target=bingPhoto,args=(word,page)))
    if(search_dict['baidu']=='true'):
        threads.append(threading.Thread(target=baiduPhoto,args=(word,page)))
    if(search_dict['sogou']=='true'):
        threads.append(threading.Thread(target=sogouPhoto,args=(word,page)))
    if(search_dict['s360']=='true'):
        threads.append(threading.Thread(target=so360Photo,args=(word,page)))
    if(search_dict['china_so']=='true'):
        threads.append(threading.Thread(target=chinaSoPhoto,args=(word,page)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    myans['status']=1
    myans=json.dumps(myans)
    print myans
    return myans

if __name__ == "__main__":
    word = "杨幂"
    search_dict={
        'baidu':'true',
        's360':'true',
        'sogou':'true',
        'china_so':'true',
        'bing':'true',
        'shen_ma':'true',
    }
    start(word,0,search_dict)
    # baiduPhoto(word,0)
    # sogouPhoto(word,0)
    # so360Photo(word,0)
    # chinaSoPhoto(word,0)
    # bingPhoto(word,0)
    # print str(time.mktime(datetime.datetime.now().timetuple()))
