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
    #print html
    soup = BeautifulSoup(html,"lxml")
    baiduRes=[]
    for item in soup.find_all("span",attrs={"class" : "hint_toprq_tips_items"}):
        #print item
        for acontent in item.find_all("a"):
            #print acontent.get_text()
            baiduRes.append(acontent.get_text())
    mutex.acquire()
    myans['baidu']=baiduRes
    mutex.release()

def baiduRecommend(word,flag=False):
    url="http://220.181.111.188/s?wd="+word+"&pn=1"
    try:
        response = requests.get(url,timeout=10)
    except:
        print "get recommend from baidu failed"
        return
    result = response.text
    #print result
    # baiduExtract(result)
    baiduExtractFor(result)

def so360ExtractFor(html):
    global mutex
    # print html
    so360Res=[]
    soup = BeautifulSoup(html,"lxml")
    for item in soup.find_all("span",attrs={"class" : "so-pdr-box"}):
        #print item
        for acontent in item.find_all("a"):
            #print acontent.get_text()
            so360Res.append(acontent.get_text())
    mutex.acquire()
    myans['s360']=so360Res
    mutex.release()

def so360Recommend(word,flag=False):
    url="http://www.so.com/s?q="+word+"&pn=1"
    try:
        response = requests.get(url,timeout=5)
    except:
        print "get recommend from 360 failed"
        return
    result = response.text.encode('ISO-8859-1').decode('utf-8')
    #print result
    so360ExtractFor(result)

def chinaSoExtractFor(html):
    global mutex
    #print html
    chinaSoRes=[]
    soup = BeautifulSoup(html,"lxml")
    for item in soup.find_all("span",attrs={"class" : "hintTopItem"}):
        #print item
        for acontent in item.find_all("a"):
            #print acontent.get_text()
            chinaSoRes.append(acontent.get_text())
    mutex.acquire()
    myans['china_so']=chinaSoRes
    mutex.release()


def chinaSoRecommend(word,flag=False):
    url="http://www.chinaso.com/search/pagesearch.htm?q="+word
    try:
        response = requests.get(url,timeout=5)
    except:
        print "get recommend from china_so failed"
        return
    result = response.text
    #print result
    chinaSoExtractFor(result)

def sogouExtractFor(html):
    global mutex
    #print html
    sogouRes=[]
    soup = BeautifulSoup(html,"lxml")
    for item in soup.find_all("dl",attrs={"class" : "hint2", "id" : "float_uphint"}):
        #print item
        for acontent in item.find_all("a"):
            #print acontent.get_text()
            sogouRes.append(acontent.get_text())
    mutex.acquire()
    myans['sogou']=sogouRes
    mutex.release()


def sogouRecommend(word,flag=False):
    url="https://www.sogou.com/web?query="+word+"&page=1"
    try:
        response = requests.get(url,timeout=5)
    except:
        print "get recommend from china_so failed"
        return
    result = response.text
    #print result
    sogouExtractFor(result)

def hint_top(word, search_dict):
    global myans,mutex
    mutex = threading.Lock()
    threads=[]
    myans={}
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
    threads.append(threading.Thread(target=so360Recommend,args=(word,False)))
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    myans['status']=1
   # myans=json.dumps(myans,ensure_ascii=False)
    print myans
    return myans


if __name__ == "__main__":
    word = "苹果"
    search_dict={'baidu':'true','sogou':'false','s360':'false','bing':'false','china_so':'false','shen_ma':'false'}

    hint_top(word,search_dict)
