# encoding: utf-8
import requests
import sys
import re
import threading
import json
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf8")

def baiduExtractFor(html):
    global mutex
    soup = BeautifulSoup(html,"lxml")
    for item in soup.find_all("span",attrs={"class" : "hint_toprq_tips_items"}):
        mutex.acquire()
        for acontent in item.find_all("a"):
            key=acontent.get_text()
            #print 'get baidu key: ',key
            if(datas.has_key(key)):
                datas[key]=datas[key]+';baidu'
            else:
                datas[key]='baidu' 
        mutex.release()

def baiduRecommend(word,flag=False):
    url="http://220.181.111.188/s?wd="+word+"&pn=1"
    try:
        response = requests.get(url,timeout=10)
    except:
        print "get recommend from baidu failed"
        return
    result = response.text
    baiduExtractFor(result)

def so360ExtractFor(html):
    global mutex
    soup = BeautifulSoup(html,"lxml")
    for item in soup.find_all("span",attrs={"class" : "so-pdr-box"}):
        mutex.acquire()
        for acontent in item.find_all("a"):
            key=acontent.get_text()
            #print 'get s360 key:',key
            if(datas.has_key(key)):
                datas[key]=datas[key]+';s360'
            else:
                datas[key]='s360' 
        mutex.release()

def so360Recommend(word,flag=False):
    url="http://www.so.com/s?q="+word+"&pn=1"
    try:
        response = requests.get(url,timeout=5)
    except:
        print "get recommend from 360 failed"#'ISO-8859-1'
        return
    result = response.text.encode(response.encoding).decode('utf-8')
    so360ExtractFor(result)

def chinaSoExtractFor(html):
    global mutex
    soup = BeautifulSoup(html,"lxml")
    print "chinaso wei ni tui jian1"
    spns= soup.find_all("span",attrs={"class" : "hintTopItem"})
    print len(spns)
    for item in spns:
        mutex.acquire()
        print "chinaso wei ni tui jian oooooooooooooo"
        for acontent in item.find_all("a"):
            key=acontent.get_text()
            print 'get china_so key:',key
            if(datas.has_key(key)):
                datas[key]=datas[key]+';china_so'
            else:
                datas[key]='china_so' 
        mutex.release()

def chinaSoRecommend(word,flag=False):
    url="http://www.chinaso.com/search/pagesearch.htm?q="+word
    try:
        response = requests.get(url,timeout=5)
    except:
        print "get recommend from china_so failed"
        return
    result = response.text
    chinaSoExtractFor(result)

def sogouExtractFor(html):
    global mutex
    soup = BeautifulSoup(html,"lxml")
    for item in soup.find_all("dl",attrs={"class" : "hint2", "id" : "float_uphint"}):
        mutex.acquire()
        for acontent in item.find_all("a"):
            key=acontent.get_text()
            #print 'get sogou key:',key
            if(datas.has_key(key)):
                datas[key]=datas[key]+';sogou'
            else:
                datas[key]='sogou' 
        mutex.release()

def sogouRecommend(word,flag=False):
    url="https://www.sogou.com/web?query="+word+"&page=1"
    try:
        response = requests.get(url,timeout=5)
    except:
        print "get recommend from china_so failed"
        return
    result = response.text
    sogouExtractFor(result)

def hint_top(word, search_dict):
    global datas,mutex
    mutex = threading.Lock()
    threads=[]
    datas={}
    '''
    if(search_dict.has_key('baidu') and search_dict['baidu']=='true'):
        threads.append(threading.Thread(target=baiduRecommend,args=(word,False)))
    if(search_dict.has_key('sogou') and search_dict['sogou']=='true'):
        threads.append(threading.Thread(target=sogouRecommend,args=(word,False)))
    if(search_dict.has_key('s360') and search_dict['s360']=='true'):
        threads.append(threading.Thread(target=so360Recommend,args=(word,False)))
    if(search_dict.has_key('china_so') and search_dict['china_so']=='true'):
        threads.append(threading.Thread(target=chinaSoRecommend,args=(word,False)))
  '''
    threads.append(threading.Thread(target=baiduRecommend,args=(word,False)))
    threads.append(threading.Thread(target=sogouRecommend,args=(word,False)))
    threads.append(threading.Thread(target=so360Recommend,args=(word,False)))
    threads.append(threading.Thread(target=chinaSoRecommend,args=(word,False)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return datas


if __name__ == "__main__":
    word = "刘欢"
    search_dict={'baidu':'true','sogou':'true','s360':'true','bing':'true','china_so':'true','shen_ma':'true'}
    mydata=hint_top(word,search_dict)
    mydata = json.dumps(mydata, ensure_ascii=False)
    print mydata
