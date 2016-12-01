#encoding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")

from lxml import etree
from traceback import format_exc
from urllib2 import urlopen,Request
import time


def mfReadWebInfo(url='',timeout=300):
    try:
        webInfo = None
        request = Request(url=url)
        '''
        request.add_header('Connection','keep-alive')
        request.add_header('Cookie','QiHooGUID=C0A21040044E56529270C0BDAC87CA58.1463735613748; tso_Anoyid=11146373561315922661; __guid=15484592.2252379268149142000.1463735615807.1208; dpr=1; webp=1; stc_ls_sohome=RSU!_SSR!V(S; _S=p8khbm02k925dhl73edfia3ub4; __huid=10g1aUxma9pMZeHfvNA99wzzHGWrZAg03CYx6%2F46%2FT9Qc%3D; __sid=15484592.2252379268149142000.1463735615807.1208.1464145818990; count=2; erules=p4-1%7Cp1-12%7Cecr-1%7Cp2-4')
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')
        '''
        fd = urlopen(url=request,timeout=timeout)
        webInfo = fd.read().decode('utf-8')
        fd.close()
        return webInfo,None
    except Exception,e:
        print format_exc()
        return None,e

def parseBaike(baikeElement): #解析百科
    baikeDict={'type':1,'junaType':'baike'}
    title=None
    url=None
    abstract=''
    imgUrl=None
    try:
        title=baikeElement.xpath('./h3[@class="res-title"]/a')[0].xpath('string(.)').strip()
        url=baikeElement.xpath('./h3[@class="res-title"]/a')[0].attrib.get('href')
    except Exception:
        print format_exc()
        return None
    try:
        abstract=baikeElement.xpath('./div[contains(@class,"res-baike")]//p')[0].xpath('string(.)').strip()
    except:
        pass
    try:
        imgUrl=baikeElement.xpath('./div[contains(@class,"res-baike")]/div[@class="res-comm-img"]/a/img')[0].attrib.get('src')
    except:
        pass
    baikeDict['head']=title
    baikeDict['headUrl']=url
    baikeDict['abstract']=abstract
    baikeDict['imgUrl']=imgUrl
    return baikeDict
def parseNews(newsElement): #解析新闻
    newsDict={'type':1,'junaType':'news'}
    dataList=[]
    try:
        try:
            headTitleNode=newsElement.xpath('.//h3[@class="title"]')
            headTitle=headTitleNode[0].xpath('./a')[0].xpath("string(.)").strip() #头部标题
            headUrl=headTitleNode[0].xpath('./a')[0].attrib.get('href')
            newsDict['head']=headTitle
            newsDict['headUrl']=headUrl
        except:
            return None
        try:
            firstTitle=newsElement.xpath('.//p[contains(@class,"mh-position")]')[0].xpath('./a')[0].xpath("string(.)").strip() #第一个新闻标题
            firstUrl=newsElement.xpath('.//p[contains(@class,"mh-position")]')[0].xpath('./a')[0].attrib.get('href')
            firstNodeP=newsElement.xpath('./div/div[@class="cont"]/div[@class="mh-first gclearfix"]')
            firstImgUrl=None
            try:
                firstImgUrlNode=firstNodeP[0].xpath('./div[@class="mh-first-img"]/a/img')    
                if firstImgUrlNode is not None and len(firstImgUrlNode)>0:
                    firstImgUrl=firstImgUrlNode[0].attrib.get('src')
            except:
                pass
            firstDate=None
            firstWhere=None
            abstract=''
            try:
                abstract=firstNodeP.xpath('./div[@class="mh-first-img"]/p[@class="mh-first-cont"]')[0].xpath('string(.)').trip()
            except:
                try:
                    abstract=newsElement.xpath('.//p[@class="mh-first-cont"]')[0].xpath('string(.)').strip()
                except:
                    pass
            try:
                firstDate=firstNodeP.xpath('./div[@class="mh-first-news"]//span[@class="mh-time"]')[0].xpath("string(.)").strip() #第一个新闻日期
                firstWhere=firstNodeP.xpath('./div[@class="mh-first-news"]//span[@class="mh-origin"]')[0].xpath("string(.)").strip() #第一个新闻来源
            except Exception:
                pass
            if firstDate is None and firstWhere is None:
                try:
                    firstDateAndWhere=newsElement.xpath('.//p[contains(@class,"mh-position")]')[0].xpath('.//span')
                    firstDate=firstDateAndWhere[1].xpath("string(.)").strip() #时间
                    firstWhere=firstDateAndWhere[0].xpath("string(.)").strip() #来源
                except Exception,e:
                    print format_exc()
            firstDict={'type':'news_special','title':firstTitle,'abstract':abstract,'imgUrl':firstImgUrl,'date':firstDate,'where':firstWhere,'url':firstUrl}
            dataList.append(firstDict)
        except Exception:
            print format_exc()
        otherNodePs=newsElement.xpath('.//p[@class="gclearfix"]') #剩余的相关新闻
        if otherNodePs is not None:
            for otherNodeP in otherNodePs:
                otherTitle=otherNodeP.xpath('./a')[0].xpath("string(.)").strip() #标题
                otherUrl=otherNodeP.xpath('./a')[0].attrib.get('href')
                otherDate=otherNodeP.xpath('./span[@class="mh-time"]')[0].xpath("string(.)").strip() #时间
                otherWhere=otherNodeP.xpath('./span[@class="mh-origin"]')[0].xpath("string(.)").strip() #来源
                otherDict={'type':'news_normal','title':otherTitle,'date':otherDate,'where':otherWhere,'url':otherUrl}
                dataList.append(otherDict)
        newsDict['data']=dataList
        if len(dataList)<=0:
            return None
        return newsDict
    except Exception,e:
        print format_exc()
        return newsDict

'''
由于知乎与前面的新闻格式不一致，只获取对于的标题，未获取回答数等相关信息
'''
def parseZhihu(zhihuElements): #解析知乎
    zhihuDict={'type':1,'junaType':'zhihu'}
    dataList=[]
    try:
        try:
            headTitleNode=zhihuElements.xpath('.//h3[@class="title"]')
            headTitle=headTitleNode[0].xpath('./a')[0].xpath("string(.)").strip() #头部标题
            headUrl=headTitleNode[0].xpath('./a')[0].attrib.get('href')
            zhihuDict['head']=headTitle
            zhihuDict['headUrl']=headUrl
        except:
            return None
        moreInfoNode=zhihuElements.xpath('.//div[@class="mh-more-qus"]')[0]     
        if moreInfoNode is not None and len(moreInfoNode)>0:
            moreInfos=moreInfoNode[0].xpath('.//li[@class="mh-more-item g-clearfix"]') #所有相关信息   
            if moreInfos is not None:
                for moreInfo in moreInfos:
                    try:
                        title=moreInfo.xpath('./a')[0].xpath("string(.)").strip() #标题
                        url=moreInfo.xpath('./a')[0].attrib.get('href')
                        answer=moreInfo.xpath('./span[@class="mh-reply"]')[0].xpath("string(.)").strip() #回答
                        moreDict={'type':'zhihu_normal',"title":title,"answer":answer,'url':url} 
                        dataList.append(moreDict) 
                    except:
                        pass
        if len(dataList)<=0:
            return None
        zhihuDict['data']=dataList 
        return zhihuDict            
    except Exception,e:
        print format_exc()
        return zhihuDict

#360搜索
def s360_relateInfo(webInfo):
    try:
        tree = etree.HTML(webInfo)
        resultList=[]
        mohe_news=tree.xpath('/html/body//div[@class="g-mohe "]')
        if mohe_news is not None:
            for mohe_new in mohe_news:
                try:
                    idString=mohe_new.attrib.get('id')
                    if(idString=="mohe-news"): #新闻相关信息
                        oneList=parseNews(mohe_new)
                        if oneList is not None and len(oneList)>0:
                            resultList.append(oneList)
                    elif(idString=="mohe-biu_zhihu"): #新闻知乎相关信息
                        oneList=parseZhihu(mohe_new)
                        if oneList is not None and len(oneList)>0:
                            resultList.append(oneList)
                except Exception,e:
                    pass
        return resultList        
    except Exception,e:
        print format_exc()
        return None

if __name__ == "__main__":
    webInfo,errorInfo=mfReadWebInfo("http://www.so.com/s?q=习近平",300)
    time.sleep(3)
    s360_relateInfo(webInfo)
