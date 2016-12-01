#encoding=utf-8

from lxml import etree
from traceback import format_exc
import requests
import json

def readWebInfo(url=None,timeout=300):
    if url is None:
        return None
    try:
        response=requests.get(url=url,timeout=timeout)
        return response.text
    except Exception:
        print format_exc()
        return None

def getChinaUrl(keyword,page):
    return 'http://news.chinaso.com/newssearch.htm?q=%s&page=%s'%(keyword,page)
#中国搜索新闻获取，页面从1开始
def chinaNews_info(keyword='',page=1):
    url=getChinaUrl(keyword, page)
    chinaSuffix='http://news.chinaso.com'
    newsText=readWebInfo(url)
    if newsText is None:
        return None
    try:
        resultDict={}
        resultDict['from']='china'
        resultDict['keyword']=keyword
        resultList=[]
        tree=etree.HTML(newsText)
        newsLis=tree.xpath('/html/body/div[@class="mainWrapper clearfix"]/div[@class="resultWrapper fl"]/ol[@class="seResult"]//li[@class="reItem "]')
        if newsLis is not None and len(newsLis)>0:
            status=1
            for newsLi in newsLis:
                title=None
                newsUrl=None
                where=None
                date=None
                sameNewsNum=None
                sameNewsNumUrl=None
                oneDict={}
                try:
                    title=newsLi.xpath('./h2/a')[0].xpath('string(.)').strip() #标题
                    newsUrl=newsLi.xpath('./h2/a')[0].attrib.get('href')
                except:
                    continue
                isPicNews=False
                try:
                    picNewsNode=newsLi.xpath('./div[contains(@class,"reNewsWrapper")]/ul[@class="reNewsWrapper-pic-box"]')
                    if picNewsNode is not None and len(picNewsNode)>0:
                        isPicNews=True
                except:
                    pass
                if isPicNews: #图片新闻
                    imgUrlList=[]
                    try:
                        whereDateSameNode=newsLi.xpath('./div[contains(@class,"reNewsWrapper")]/div/p[@class="snapshot"]')
                        sameNewsNum=whereDateSameNode[0].xpath('./a')[0].xpath('string(.)').strip() #相同新闻数目
                        sameNewsNumUrl=chinaSuffix+whereDateSameNode[0].xpath('./a')[0].attrib.get('href')
                        whereAndDateStr=whereDateSameNode[0].xpath('./span')[0].xpath('string(.)').strip()
                        whereAndDateList=whereAndDateStr.split()
                        date=whereAndDateList[0] #日期
                        where=whereAndDateStr.replace(date,'').replace('-','') #来源
                    except:
                        pass
                    try:
                        imgUrlLi=newsLi.xpath('./div[contains(@class,"reNewsWrapper")]/ul[@class="reNewsWrapper-pic-box"]//li')[0]
                        imgAs=imgUrlLi.xpath('.//a')
                        for imgA in imgAs:
                            tempImgUrl=imgA.xpath('./img')[0].attrib.get('src')
                            imgUrlList.append(tempImgUrl)
                    except:
                        pass
                    oneDict['type']='picNews' #表示是图片新闻
                    oneDict['imgUrls']=imgUrlList
                else: #普通新闻
                    imgUrl=None
                    abstract=None
                    try:
                        imgNode=newsLi.xpath('./div[contains(@class,"reNewsWrapper")]/div[@class="reNewsImgWrapper fl"]/div[@class="imgVM"]/a//img')
                        imgUrl=imgNode[0].attrib.get('src')
                    except:
                        pass
                    reNewsContLNode=newsLi.xpath('./div[contains(@class,"reNewsWrapper")]/div[@class="reNewsContL fr"]')
                    try:
                        abstract=reNewsContLNode[0].xpath('./p')[0].xpath('string(.)').strip() #摘要
                    except:
                        try:
                            abstract=newsLi.xpath('./div[contains(@class,"reNewsWrapper")]')[0].xpath('.//p')[0].xpath('string(.)').strip()
                        except:
                            pass
                    try:
                        whereDateSameNode=reNewsContLNode[0].xpath('./p[@class="snapshot"]')
                        sameNewsNum=whereDateSameNode[0].xpath('./a')[0].xpath('string(.)').strip() #相同新闻数目
                        sameNewsNumUrl=chinaSuffix+whereDateSameNode[0].xpath('./a')[0].attrib.get('href')
                        whereAndDateStr=whereDateSameNode[0].xpath('./span')[0].xpath('string(.)').strip()
                        whereAndDateList=whereAndDateStr.split()
                        date=whereAndDateList[0] #日期
                        where=whereAndDateStr.replace(date,'').replace('-','') #来源                        
                    except:
                        try:
                            whereDateSameNode=newsLi.xpath('.//p[@class="snapshot"]')
                            sameNewsNum=whereDateSameNode[0].xpath('./a')[0].xpath('string(.)').strip() #相同新闻数目
                            sameNewsNumUrl=chinaSuffix+whereDateSameNode[0].xpath('./a')[0].attrib.get('href')
                            whereAndDateStr=whereDateSameNode[0].xpath('./span')[0].xpath('string(.)').strip()
                            whereAndDateList=whereAndDateStr.split()
                            date=whereAndDateList[0] #日期
                            where=whereAndDateStr.replace(date,'').replace('-','') #来源                                 
                        except:
                            pass
                    oneDict['type']='normalNews' #表示是普通新闻
                    oneDict['imgUrl']=imgUrl
                    oneDict['abstract']=abstract
                oneDict['title']=title
                oneDict['url']=newsUrl
                oneDict['where']=where
                oneDict['date']=date
                oneDict['sameNewsNum']=sameNewsNum
                oneDict['sameNewsUrl']=sameNewsNumUrl
                resultList.append(oneDict) 
        if len(resultList)<=0:
            resultDict['status']=0
            resultDict['data']=None
        else:               
            resultDict['status']=1
            resultDict['data']=resultList    
        return resultDict
    except Exception:
        print format_exc()
        return None  
    
if __name__=="__main__":
    mydata=chinaNews_info(keyword="苹果",page=1) 
    mydata = json.dumps(mydata)
    print mydata       