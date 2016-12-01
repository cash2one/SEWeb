#coding:utf-8

import requests
import sys
import re
import threading
import json

reload(sys)
sys.setdefaultencoding("utf8")

def baiduSuggestion(word,delay=False):
    global mutex
    url = "http://suggestion.baidu.com/su?wd="+word
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get suggestion from baidu failed"
        return

    result = response.text
    pattern = r"\[(.*?)\]"
    matchObj = re.findall(pattern,result,re.M)
    if(len(matchObj) > 0):
        mutex.acquire()
        # print matchObj[0]
        pattern = "\"(.*?)\""
        matchObj = re.findall(pattern,matchObj[0],re.M)
        for w in matchObj:
            # print w
            key=w
            if(datas.has_key(key)):
                datas[key] = datas[key]+";baidu"
            else:
                datas[key] = "baidu"
        mutex.release()

def sogouSuggestion(word,delay=False):
    global mutex
    url="https://www.sogou.com/suggnew/ajajjson?key="+word+"&type=web&ori=yes&pr=web&abtestid=0&ipn=false"
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get suggestion from sogou failed"
        return

    result = response.text
    pattern = r",\[(.*?)\]"
    matchObj = re.findall(pattern,result,re.M)
    if(len(matchObj) > 0):
        mutex.acquire()
        # print matchObj[0]
        for w in matchObj[0].split('",'):
            w = '"' + re.sub('"','',w) + '"'
            # print "["+w+"]"
            if(len(w)>0):
                key = eval("u"+w)
                # key = key[1:-1]
                if(datas.has_key(key)):
                    datas[key] = datas[key] + ";sogou";
                else:
                    datas[key] = "sogou"
        mutex.release()

def getBingCVID():
    url = "http://cn.bing.com/"
    try:
        response = requests.get(url,timeout=2)
        html_text = response.text
        try:
            # IID= re.findall("<div id=\"lap_w\" data-ajaxiid=\"(.*)\" data-date=\"",html_text)[0]
            m= re.search("IG:\"(.*)\",EventID:",html_text)
            if m:
                IG= m.group(1)
#                print "cvid="+IG
                return IG
        except Exception as e:
            print(e)
    except:
        print "Get Bing cvid error"
    return None

def bingSuggestion(word,delay=False):
    global mutex
    # cvid = "74EB888789494B158BBA8A3950C3ED3F"
    # cvid = "F696908625C84BB79E4CF88B64485758"
    cvid = getBingCVID()
    if(cvid == None):
        return
    url="http://cn.bing.com/AS/Suggestions?pt=page.serp&bq="+word+"&mkt=zh-cn&qry="+word+"&cp="+str(len(word))+"&o=hs&css=1&cvid="+cvid
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get suggestion from bing failed"
        return

    result = response.text
    # print result
    # pattern = r"query=(.*?) nav"
    pattern = r"query=\"(.*?)\""
    matchObj = re.findall(pattern,result,re.M)
    if(len(matchObj)>0):
        # print matchObj
        mutex.acquire()
        for obj in matchObj:
            # key=obj[1:-1]
            key=obj
            if(datas.has_key(key)):
                datas[key] = datas[key]+";bing"
            else:
                datas[key] = "bing"
        mutex.release()

def so360Suggest(word,delay=False):
    global mutex
    url = "http://sug.so.360.cn/suggest/word?callback=suggest_so&encodein=utf-8&encodeout=utf-8&word=" + word
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get suggestion from so360 failed"
        return

    result = response.text
    pattern = r"\[(.*?)\]"
    matchObj = re.findall(pattern, result, re.M)
    if(len(matchObj) > 0):
        mutex.acquire()
        for obj in matchObj[0].split(","):
            key=obj[1:-1]
            if(datas.has_key(key)):
                datas[key] = datas[key]+";so360"
            else:
                datas[key] = "so360"
        mutex.release()
def shenMaSuggest(word,delay=False):
    global mutex
    url=""
    try:
        response=requests.get(url,timeout=2)
    except:
        print "get suggestion from shenma failed"
        return
    result=respones.text
    print result
    
def chinasoSuggest(word,delay=False):
    global mutex
    url = "http://www.chinaso.com/search/suggest?callback=jsonpHandle&k=" + word
    try:
        response = requests.get(url,timeout=2)
    except:
        print "get suggestion from chinaso failed"
        return

    result = response.text
    # print result
    pattern = r"\[(.*?)\]"
    matchObj = re.findall(pattern, result, re.M)
    if(len(matchObj) > 0):
        mutex.acquire()
        for obj in matchObj[0].split(","):
            obj = '"' + re.sub('"','',obj) + '"'
            key=eval("u"+obj)
            if(datas.has_key(key)):
                datas[key] = datas[key]+";chinaSo"
            else:
                datas[key] = "chinaSo"
        mutex.release()

def start(word):
    global datas,mutex
    mutex = threading.Lock()
    threads=[]
    datas={}
    #if(search_dict['bing']=='true'):
     #   threads.append(threading.Thread(target=bingSuggestion,args=(word,False)))
    #if(search_dict['baidu']=='true'):
    #    threads.append(threading.Thread(target=baiduSuggestion,args=(word,False)))
    #if(search_dict['sogou']=='true'):
    #    threads.append(threading.Thread(target=sogouSuggestion,args=(word,False)))
    #if(search_dict['s360']=='true'):
    #    threads.append(threading.Thread(target=so360Suggest,args=(word,False)))
    #if(search_dict['china_so']=='true'):
    #    threads.append(threading.Thread(target=chinasoSuggest,args=(word,False)))
    #if(search_dict['shen_ma'] == 'true'):
    #    threads.append(threading.Thread(target=baiduSuggestion,args=(word,False,False)))

    threads.append(threading.Thread(target=bingSuggestion,args=(word,False)))
    threads.append(threading.Thread(target=baiduSuggestion,args=(word,False)))
    threads.append(threading.Thread(target=sogouSuggestion,args=(word,False)))
    threads.append(threading.Thread(target=so360Suggest,args=(word,False)))
    threads.append(threading.Thread(target=chinasoSuggest,args=(word,False)))   
 
    for t in threads:
        t.start()
    for t in threads:
        t.join()



    if "" in datas.keys():
        datas.pop("",None)

    #for key in datas.keys():
    #    print "["+key+"]-----"+datas[key]

    #datas = json.dumps(datas,ensure_ascii=False)
    #print datas
    return datas

if __name__ == "__main__":
    word = "苹果"

    search_dict={
        'baidu':'false',
        's360':'true',
        'sogou':'false',
        'china_so':'false',
        'bing':'true',
        'shen_ma':'false',
    }
    start(word)
    # stri = "\"爱情保卫战\",\"爱情公寓\",\"爱情电影\",\"爱情公寓5\",\"爱情电影网,天海\",\"爱奇艺\",\"爱情公寓4\",\"爱情公寓3\"";
    # print stri
    # pattern = "\"(.*?)\""
    # matchObj = re.findall(pattern,stri,re.M)
    # for obj in matchObj:
    #     print obj
    # getBingCVID()

