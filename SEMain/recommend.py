# coding:utf-8

import requests
import sys
import re
import json
import base64
import time,datetime
import threading
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf8")

def baiduSrcTransfor(link):
    res=link.split("/")
    return "https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/"+res[4]

#右侧推荐
def baiduExtract(html):
    global mutex
    baiduRes=[]
    soup = BeautifulSoup(html,"lxml")
    # for content in soup.find_all("div",attrs={"opr-recommends-merge-content"}):
    index=0
    print "baidu start"
    for content in soup.find_all("div",attrs={"cr-content"}):
        if index>=1 :
            break
        print "baidu listening-------------"
        index=index+1
        titleDiv = content.find_all("div",attrs={"class":"cr-title c-clearfix"})
        # panelDiv = content.find_all("div",attrs={"class":"opr-recommends-panel"})
        panelDiv = content.find_all("div",attrs={"class":re.compile("opr-recommends-.*panel")})
        
        for i in xrange(0,len(titleDiv)):
            #获取文字组标题
            mgroup={}
            titleItem = titleDiv[i]
            pattern = "<span title=\"(.*?)\""
            matchObj = re.findall(pattern,titleItem.__str__())
            if matchObj:
                # print matchObj[0]+"=========================="
                mgroup['title']=matchObj[0]
                # print mgroup['title']

            mdatas=[]
            panelItem = panelDiv[i]
            items = panelItem.find_all("div",attrs={"class":re.compile("opr-recommends-.*item")})
            for j in range(0,len(items)):
                #if j%4 != 3:
                try:
                    mitem={}
                    #获取百度搜索引擎右侧推荐item的文字部分
                    pattern = "rsv_re_ename\':\'(.*?)\'";
                    matchObj = re.search(pattern,items[j].__str__(),re.M)
                    if matchObj:
                        # print matchObj.group(1)
                        mitem['desc']=matchObj.group(1)
                        print mitem['desc']
                    #获取百度搜索引擎右侧推荐的图片来源链接地址
                    pattern = "(src=\"|data-img=\")(.*?)\""
                    matchObj = re.search(pattern,items[j].__str__(),re.M)
                    if matchObj:
                        # print "src:"+matchObj.group(2).replace("amp;","")
                        srcLink=matchObj.group(2).replace("amp;","")
                        mitem['src']=baiduSrcTransfor(srcLink)
                        # print mitem['src']
                    #获取百度搜索引擎右侧推荐的图片点击链接地址
                    pattern = "<a href=\"(.*?)\""
                    matchObj = re.search(pattern,items[j].__str__(),re.M)
                    if matchObj:
                        # print "http://www.baidu.com"+matchObj.group(1).replace("amp;","")
                        mitem['target']="http://www.baidu.com"+matchObj.group(1).replace("amp;","")
                        # print ""
                    mdatas.append(mitem)
                except:
                    print "baidu trans error"
            mgroup['data']=mdatas
            baiduRes.append(mgroup)
        # print json.dumps(baiduRes,ensure_ascii=False)
    mutex.acquire()
    myans['baidu']=baiduRes
    mutex.release()

def baiduRecommend(word,flag=False):
    url="http://www.baidu.com/s?wd="+str(word)+"&pn=1"
    try:
        response = requests.get(url,timeout=5)
    except:
        print "get recommend from baidu failed"
        return
    result = response.text
    baiduExtract(result)
    # baiduExtractFor(result)

def sogouExtract(html):
    global mutex
    matchObj=re.search("var kmapRight = ({.*?});",html)
    sogouRes=[]
    if matchObj:
        jsonStr=matchObj.group(1)
        jsonObj = json.loads(jsonStr)
        soup = BeautifulSoup(jsonObj['xml'],"lxml")
        for content in soup.find_all("attribute"):
            mgroup={}
            pattern = "name=\"(.*?)\""
            matchObj = re.search(pattern,content.__str__(),re.M)
            if matchObj:
                mgroup['title']=matchObj.group(1)
                # print matchObj.group(1)
            mdatas=[]
            for element in content.find_all("element"):
                mitem={}
                #搜狗明医搜索的右侧推荐的描述
                pattern = "name=\"(.*?)\""
                matchObj = re.search(pattern,element.__str__(),re.M)
                if matchObj:
                    desc=matchObj.group(1)
                    mitem['desc']=desc
                #搜狗搜索的右侧推荐的src
                pattern="picaddress=\"(.*?)\""
                # pattern = "wapurl=\"(.*?)\""
                matchObj = re.search(pattern,element.__str__(),re.M)
                if matchObj:
                    src=matchObj.group(1)
                    mitem['src']=src
                #搜狗搜索的右侧点击链接
                target="http://www.sogou.com/web?ie=utf8&w=01029901&p=71330100&dp=1&query="+desc+"&clickArea=1"
                mitem['target']=target
                mdatas.append(mitem)
            mgroup['data']=mdatas
            sogouRes.append(mgroup)
        # print json.dumps(sogouRes,ensure_ascii=False)
        mutex.acquire()
        myans['sogou']=sogouRes
        mutex.release()

def sogouRecommend(word,flag=False):
    url="http://www.sogou.com/web?query="+str(word)+"&page=1"
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get recommend from sogou failed"
        return
    result = response.text
    # print result
    sogouExtract(result)

def so360Extract(html):
    global mutex
    so360Res=[]
    soup = BeautifulSoup(html,"lxml")
    for content in soup.find_all("div",attrs={"class":"mh-box "}):
        mgroup={}
        for title in content.find_all("h3",attrs={"class":"title"}):
            # print title['title']
            mgroup['title']=title['title']
        mdatas=[]
        for items in content.find_all("a",attrs={"class":"mh-img-link"}):
            mitem={}
            # desc
            # print items["title"]
            mitem['desc']=items["title"]
            # target
            # print items["href"]
            mitem['target']=items["href"]
            # src
            pattern = "src=\"(.*?)\""
            matchObj = re.search(pattern,items.__str__(),re.M)
            if matchObj:
                # print matchObj.group(1)
                mitem['src'] = matchObj.group(1)
            mdatas.append(mitem)
        mgroup['data']=mdatas
        so360Res.append(mgroup)
    # print json.dumps(so360Res,ensure_ascii=False)
    mutex.acquire()
    myans['360']=so360Res
    mutex.release()

def so360Recommend(word,flag=False):
    url="http://www.so.com/s?ie=utf-8&shb=1&src=360sou_newhome&q="+str(word)
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get recommend from 360so failed"#'ISO-8859-1'
        return
    result = response.text.encode(response.encoding).decode('utf-8')
    # print result
    so360Extract(result)

def chinaSoExtract(html):
    global mutex
    soup = BeautifulSoup(html,"lxml")
    chinaRes=[]
    contents = soup.find_all("div",attrs={"class":"sideMod"})
    for content in contents:
        try:
            if content.has_attr('id'):
                print "...."
            else:
                mgroup={}
                title = content.find("h3")
                mgroup['title']=title.get_text()
                mdatas=[]
                for items in content.find_all("td"):
                    target="http://www.chinaso.com"+items.a['href']
                    target.replace("amp;","")
                    mitem={}
                    mitem['desc']=items.img['alt']
                    mitem['target']=target
                    mitem['src']=items.img['src']
                    mdatas.append(mitem)
                mgroup['data']=mdatas
                chinaRes.append(mgroup)
                # print items.img['alt']
                # print target
                # print items.img['src']
        except:
            print "chinaSO recommend error"
    mutex.acquire()
    myans['chinaSo']=chinaRes
    mutex.release()

def chinaSoRecommend(word,flag=False):
    # url="http://www.chinaso.com/search/pagesearch.htm?q="+str(word)+"&t="+str(time.mktime(datetime.datetime.now().timetuple()))
    url="http://www.chinaso.com/search/pagesearch.htm?q="+str(word)
    try:
        response = requests.get(url,timeout=3)
    except:
        print "get recommend from chinaso failed"
        return
    result = response.text
    # print result
    chinaSoExtract(result)

def bingExtract(html):
    global mutex
    soup = BeautifulSoup(html,"lxml")
    bingRes=[]
    for content in soup.find_all("div",attrs={"class":"b_re"}):
        mgroup={}
        title = content.find(attrs={"class":"re_twrap"})
        # print title.get_text()
        mgroup['title']=title.get_text()
        mdatas=[]
        for item in content.find_all("div",attrs={"class":"cico"}):
            mitem={}
            #desc
            # print item.div["data-title"]
            mitem['desc']=item.div["data-title"]
            #src
            # print item.div["data-src"]
            mitem['src']=item.div["data-src"]
            #target
            mitem['target']= "http://cn.bing.com"+item.a["href"]
            # print "http://cn.bing.com"+item.a["href"]
            mdatas.append(mitem)
        # print ""
        mgroup['data']=mdatas
        bingRes.append(mgroup)
    # print json.dumps(bingRes,ensure_ascii=False)
    mutex.acquire()
    myans['bing']=bingRes
    mutex.release()

def bingRecommend(word,flag=False):
    url='https://www.bing.com/search?q='+str(word)+'&first=1'
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get recommend from bing failed"
        return
    result=response.text
    bingExtract(result)

def shenmaExtract(html):
    soup = BeautifulSoup(html,"lxml")
    for content in soup.find_all("div",attrs={"class":"rankbox"}):
        title =re.search("<div class=\"title\">(.*?)</div>",content.__str__())
        if title:
            pass#print title.group(1)
        for item in content.find_all("a"):
            pass#print item
            #print ds
           # print ""

def shenmaRecommend(word,flag=False):
    base64_text = base64.encodestring(word).strip()
    base64_text = base64_text.replace("+","!")
    url=u'http://aibing.cc/shenma/'+base64_text+u'.html'
    #print "url:"+url
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get recommen from shenma failed"
        return
    result = response.text
    # print result
    shenmaExtract(result)

def start(word,search_dict):
    global myans,mutex
    mutex = threading.Lock()
    threads=[]
    myans={}
    if(search_dict['bing']=='true'):
        threads.append(threading.Thread(target=bingRecommend,args=(word,False)))
    if(search_dict['baidu']=='true'):
        threads.append(threading.Thread(target=baiduRecommend,args=(word,False)))
    if(search_dict['sogou']=='true'):
        threads.append(threading.Thread(target=sogouRecommend,args=(word,False)))
    if(search_dict['s360']=='true'):
        threads.append(threading.Thread(target=so360Recommend,args=(word,False)))
    if(search_dict['china_so']=='true'):
        threads.append(threading.Thread(target=chinaSoRecommend,args=(word,False)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    myans['status']=1
    myans=json.dumps(myans,ensure_ascii=False)
    #print myans
    return myans

if __name__ == "__main__":
    word = "百度"
    # word = "百度"
    word="凡人修仙传"
    # word="网易云音乐"
    search_dict={
        'baidu':'true',
        's360':'true',
        'sogou':'true',
        'china_so':'true',
        'bing':'true',
        'shen_ma':'true',
    }
    start(word,search_dict)
