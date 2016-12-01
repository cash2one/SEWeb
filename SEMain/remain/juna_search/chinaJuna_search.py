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
from lxml import etree
from traceback import format_exc
from urllib2 import urlopen,Request
import time
import types

from selenium import webdriver

'''
返回结果格式：
[[{"head":'',"type":''},{},{}],[{"head":'',"type":''},{},{}]]
新闻
[{"head":"","type":"news"},{'title':'','imgUrl':'','date':'','where':''},{'title':'','date':'','where':''}]
国搜问答
[{"head":"","type":"aq"},{'title':'','answer':'','date':''},{'title':'','answer':'','date':''}]
'''

def parseNews(newsElement): #解析国搜新闻
    oneList=[]
    try:
        lunabox_news=newsElement.find_element_by_xpath('./div[@id="lunabox_news"]')
        if lunabox_news is not None: 
            headTitle=lunabox_news.find_element_by_xpath('./h2/a').text  #聚纳新闻标题
            headDict={'head':headTitle,'type':'news'}
            oneList.append(headDict)
            #print 'head',headTitle,'type','news'
            allNewsLis=lunabox_news.find_elements_by_xpath('./ul[@class="reNews"]/li')
            if allNewsLis is not None and len(allNewsLis)>0:
                for allNewsLi in allNewsLis:
                    try:
                        classStr=allNewsLi.get_attribute('class')
                        #classstr=classStr.encode('utf-8')
                        if classStr is None or classStr=='': #普通的li元素
                            normalTitle=allNewsLi.find_element_by_xpath('./a').text #文章标题
                            normalDate=allNewsLi.find_element_by_xpath('./span[@class="reNewsDate fr"]').text #文章日期
                            normalWhere=allNewsLi.find_element_by_xpath('./span[@class="reNewsFrom"]').text #文章来源
                            normalDict={'title':normalTitle,'date':normalDate,'where':normalWhere}
                            #print 'title',normalTitle,'date',normalDate,'where',normalWhere
                            oneList.append(normalDict)
                        elif classStr=="reNewsTop" or classStr==u'reNewsTop': #第一个li元素
                            firstTitle=allNewsLi.find_element_by_xpath('./a').text #文章标题
                            firstNode=allNewsLi.find_elements_by_xpath('.//span[@class="reNewsInfo"]')
                            firstDate=None
                            firstWhere=None
                            if firstNode is not None and len(firstNode)>0:
                                firstWhere=firstNode[0].find_element_by_xpath('./span[@class="reNewsFrom"]').text
                                firstDate=firstNode[0].text.replace(firstWhere,'')
                            firstDict={'title':firstTitle,'date':firstDate,'where':firstWhere}
                            #print 'title',firstTitle,'date',firstDate,'where',firstWhere
                            oneList.append(firstDict)
                    except Exception,e:
                        print format_exc()
        return oneList
    except Exception,e:
        print format_exc()
        return None
    
def parseAQ(aqElement): #解析国搜问答
    oneList=[]
    try:
        boxAQLeftA=aqElement.find_element_by_xpath('./div[@id="boxAQLeftA"]')
        if boxAQLeftA is not None: 
            headTitle=boxAQLeftA.find_element_by_xpath('./h2/a').text  #聚纳问答标题
            headDict={'head':headTitle,'type':'aq'}
            oneList.append(headDict)
            #print 'head',headTitle,'type','news'
            allNewsLis=boxAQLeftA.find_elements_by_xpath('./ul[@class="reNews"]/li')
            if allNewsLis is not None and len(allNewsLis)>0:
                for allNewsLi in allNewsLis:
                    try:
                        classStr=allNewsLi.get_attribute('class') #classStr没有的时候不为空,而是''
                        if classStr is None or classStr=='': #普通的li元素
                            normalTitle=allNewsLi.find_element_by_xpath('./a').text #问答标题
                            normalDate=allNewsLi.find_element_by_xpath('./span[@class="fr"]/span[@class="reNewsDate fr"]').text #问答日期
                            normalAnswer=allNewsLi.find_element_by_xpath('./span[@class="fr"]/span[@class="aqBoxTQ"]').text #回答数
                            normalDict={'title':normalTitle,'date':normalDate,'answer':normalAnswer}
                           # print 'title',normalTitle,'date',normalDate,'answer',normalAnswer
                            oneList.append(normalDict)
                        elif classStr=="reNewsTop": #第一个li元素
                            firstNode=allNewsLi.find_element_by_xpath('./div[@class="aqBoxTopTitle clearfix"]')
                            firstTitle=None
                            firstDate=None
                            firstWhere=None
                            if firstNode is not None:
                                firstTitle=firstNode.find_element_by_xpath('./a').text
                                firstAnswer=firstNode.find_element_by_xpath('./span[@class="fr"]/b[@class="aqBoxTQ"]').text #回答数
                                firstDate=firstNode.find_element_by_xpath('./span[@class="fr"]/b[@class="aqBoxTT"]').text #日期
                            firstDict={'title':firstTitle,'date':firstDate,'where':firstAnswer}
                           # print 'title',firstTitle,'date',firstDate,'where',firstAnswer
                            oneList.append(firstDict)
                    except Exception,e:
                        print format_exc()
        return oneList
    except Exception,e:
        print format_exc()
        return None
def getWebPage(url): #获取页面
    try:
        driver = webdriver.Firefox()
        driver.get(url)
        return driver
    except Exception,e:
        print format_exc()
        return None
#中国搜索
def china_relateInfo(url):
    try:
        resultList=[]
        driver=getWebPage(url)
        if driver is not None:
            seResult=driver.find_elements_by_xpath('/html/body/div[@class="mainWrapper clearfix"]/div[@class="resultWrapper fl"]/ol[@class="seResult"]')
            if seResult is not None and len(seResult)>0:
                allResult=seResult[0].find_elements_by_xpath('.//li[@class="reItem "]')
                if allResult is not None and len(allResult)>0:
                    for result in allResult:
                        try:
                            newsElement=result.find_elements_by_xpath('./div[@id="lunabox_news"]')
                            aqElement=result.find_elements_by_xpath('./div[@id="boxAQLeftA"]')
                            if newsElement is not None and len(newsElement)>0: #存在新闻相关聚纳
                                oneList=parseNews(result)
                                if oneList is not None and len(oneList)>0:
                                    resultList.append(oneList)
                            if aqElement is not None and len(aqElement)>0: #存在国搜问答相关聚纳
                                oneList=parseAQ(result)
                                if oneList is not None and len(oneList)>0:
                                    resultList.append(oneList)
                        except Exception,e:
                            print format_exc()
        driver.quit()
        return resultList
    except Exception,e:
        print format_exc()
        return None

if __name__ == "__main__":
    china_relateInfo("http://www.chinaso.com/search/pagesearch.htm?q=李克强")
