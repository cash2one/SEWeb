#encoding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")
'''
中国搜索相关聚纳信息
v1.0
新闻聚纳获取没有问题
国搜问答暂时没有问题
'''
import  requests
from traceback import format_exc
import json
import time

def filterText(text): #过滤文本
    text=text.replace('<em>','')
    text=text.replace('</em>','')
    text=text.replace('&amp;','')
    text=text.replace('&quot;','')
    return text

def parseNews(keyword): #新闻聚纳
    newsDict={'type':1,'junaType':'news','head':keyword+'最新相关消息_国搜新闻','headUrl':None}
    dataList=[]
    header={'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection':'keep-alive',
            'Host':'www.chinaso.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
        }
    #中国搜索新闻聚纳访问地址
    url='http://www.chinaso.com/search/api/news/?q=intitle:%s&img=-1&rn=5&order=time'%keyword
    response=None
    try:
        response=requests.get(url,headers=header,timeout=300)
    except:
        print "get news juna from chinaso failed"
        return None
    if response is not None: #直接返回json文件
        try:
            newsData=response.text
            try:
                newsData=json.loads(newsData)
                for oneDataDict in newsData:
                    title=oneDataDict.get('title')
                    if title=='':
                        continue
                    if title is not None:
                        title=filterText(title)
                    url=oneDataDict.get('url',None)
                    where=oneDataDict.get('site',None)
                    abstract=oneDataDict.get('snippet','')
                    if abstract=='':
                        abstract=oneDataDict.get('source')
                    if abstract is not None:
                        abstract=filterText(abstract)
                    date=None
                    try:
                        timeStamp=oneDataDict.get('time')
                        timeArray = time.localtime(timeStamp)
                        date= time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    except:
                        pass
                    images=oneDataDict.get('images')
                    imgUrl=None
                    if images is not None and len(images)>0: #只拿第一张图片
                        imgUrl=images[0].get('url',None)
                    oneDict={'type':'news_special','title':title,'abstract':abstract,'imgUrl':imgUrl,'date':date,'where':where,'url':url}
                    dataList.append(oneDict)
            except:
                return None
            newsDict['data']=dataList
            return  newsDict
        except Exception:
            print format_exc()
    return None        
def parseWenDa(keyword): #问答聚纳
    newsDict={'type':1,'junaType':'wenda','head':keyword+'_国搜问答','headUrl':None}
    dataList=[]
    header={
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection':'keep-alive',
            'Host':'wenda.chinaso.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    }
    #中国搜索问答聚纳访问地址
    url='http://wenda.chinaso.com/search/api/query?q=%s&rn=5&_mal=80'%keyword   
    response=None
    try:
        response=requests.get(url,headers=header,timeout=300)      
    except:
        print "get news juna from chinaso failed"
        return None
    if response is not None: #返回的结果需要处理下
        wenDaData=response.text  
        try:
            wenDaData=json.loads(wenDaData)
            jsonList=wenDaData.get('data').get('list')
            for oneDict in jsonList:
                title=oneDict.get('title',None)
                if title is None:
                    continue
                if title is not None:
                    title=filterText(title)
                url=oneDict.get('url')
                answerCount=oneDict.get('answersCount')
                date=None
                try:
                    timeStamp=oneDict.get('time')
                    timeArray = time.localtime(timeStamp)
                    date= time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                except:
                    pass
                bestAnswer=oneDict.get('best_answer')
                if bestAnswer is not None:
                    bestAnswer=filterText(bestAnswer)
                desc=oneDict.get('desc')
                if desc is not None:
                    desc=filterText(desc)
                dict={'type':'wenda_special','title':title,'desc':desc,'answerCount':answerCount,'bestAnswer':bestAnswer,'date':date,'url':url}
                dataList.append(dict)
        except:
            return None
        if len(dataList)<=0:
            return None
        newsDict['data']=dataList
        return newsDict
    return None
if __name__=="__main__":
    #print parseNews("习近平")
    print parseWenDa("习近平")
    