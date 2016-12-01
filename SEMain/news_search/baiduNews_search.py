#encoding=utf-8

import requests
from lxml import etree
from traceback import format_exc

def readWebInfo(url=None,timeout=300):
    if url is None:
        return None
    try:
        response=requests.get(url=url,timeout=timeout)
        return response.text
    except Exception:
        print format_exc()
        return None
    
def baiduSrcTransfor(link):
    res=link.split("/")
    return "https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/"+res[len(res)-1]

def getBaiduUrl(keyword="",page=1):
    return 'http://news.baidu.com/ns?word=%s&pn=%s&ct=1&tn=news&ie=utf-8&bt=0&et=0'%(keyword,10*(page-1))
#根据关键字获取百度新闻，page从1开始
def baiduNews_info(keyword="",page=1):
    url=getBaiduUrl(keyword, page)
    baidunewSuffix='http://news.baidu.com'
    newsText=readWebInfo(url)
    if newsText is None:
        return None
    try:
        resultDict={}
        resultDict['from']='baidu'
        resultDict['keyword']=keyword
        resultList=[]
        tree = etree.HTML(newsText)
        news_divs=tree.xpath('/html/body/div[@id="wrapper"]//div[@class="result"]') #该页的新闻
        if news_divs is not None and len(news_divs)>0:
            for news_div in news_divs:
                title=None
                newsUrl=None
                imgUrl=None
                where=None
                date=None
                abstract=None
                sameNewsNum=None
                sameNewsNumUrl=None
                try:
                    title=news_div.xpath('./h3/a')[0].xpath('string(.)').strip() #新闻标题
                except: #获取不到标题则跳过
                    continue
                try:
                    newsUrl=news_div.xpath('./h3/a')[0].attrib.get('href') #新闻链接
                except:
                    pass
                try:
                    detailInfoNode=news_div.xpath('./div[@class="c-summary c-row c-gap-top-small"]')
                    if detailInfoNode is None or len(detailInfoNode)<=0:
                        detailInfoNode=news_div.xpath('./div[@class="c-summary c-row "]')
                    try: #有些新闻没有图片链接
                        imgUrl=detailInfoNode[0].xpath('./div[@class="c-span6"]/a/img')[0].attrib.get('src') #新闻图片链接
                    except:
                        try:
                            imgUrl=news_div.xpath('.//img[@class="c-img c-img6"]')[0].attrib.get('src')
                        except:
                            pass
                    if imgUrl is not None:
                        imgUrl=baiduSrcTransfor(imgUrl)
                    try:
                        authorAndDate=detailInfoNode[0].xpath('./div[@class="c-span18 c-span-last"]/p[@class="c-author"]')[0].xpath('string(.)').strip()
                        authorData=authorAndDate.split() #来源和日期以空格分割
                        where=authorData[0]
                        date=authorData[1] 
                    except:
                        try:
                            authorAndDate=detailInfoNode[0].xpath('.//p[@class="c-author"]')[0].xpath('string(.)').strip()
                            authorData=authorAndDate.split() #来源和日期以空格分割
                            where=authorData[0]
                            date=authorData[1]                            
                        except:
                            pass
                    try:
                        abstractList=detailInfoNode[0].xpath('./div[@class="c-span18 c-span-last"]/text()') #摘要
                        abstract=''.join(abstractList)
                        if abstract=='':
                            try:
                                abstractList=detailInfoNode[0].xpath('./text()') #摘要
                                abstract=" ".join(abstractList)
                            except:
                                pass                            
                    except:
                        try:
                            abstractList=detailInfoNode[0].xpath('./text()') #摘要
                            abstract=" ".join(abstractList)
                        except:
                            pass
                    try:
                        allA=detailInfoNode[0].xpath('./div[@class="c-span18 c-span-last"]/span[@class="c-info"]/a')
                        if allA is not None and len(allA)>1: #只有出现两个链接的时候才会有相同新闻这一项
                            sameNewsNum=detailInfoNode[0].xpath('./div[@class="c-span18 c-span-last"]/span[@class="c-info"]/a')[0].xpath('string(.)').strip() #相同新闻数目
                            sameNewsNumUrl=baidunewSuffix+detailInfoNode[0].xpath('./div[@class="c-span18 c-span-last"]/span[@class="c-info"]/a')[0].attrib.get('href') 
                        else:
                            try:
                                allA=detailInfoNode[0].xpath('./span[@class="c-info"]/a')
                                if allA is not None and len(allA)>1: #只有出现两个链接的时候才会有相同新闻这一项
                                    sameNewsNum=allA[0].xpath('string(.)').strip() #相同新闻数目
                                    sameNewsNumUrl=baidunewSuffix+allA[0].attrib.get('href') 
                            except:
                                pass                              
                    except:
                        try:
                            allA=detailInfoNode[0].xpath('./span[@class="c-info"]/a')
                            if allA is not None and len(allA)>1: #只有出现两个链接的时候才会有相同新闻这一项
                                sameNewsNum=allA[0].xpath('string(.)').strip() #相同新闻数目
                                sameNewsNumUrl=baidunewSuffix+allA[0].attrib.get('href') 
                        except:
                            pass                     
                except:
                    pass
                oneDict={'type':'normalNews','title':title,'url':newsUrl,'imgUrl':imgUrl,'where':where,'date':date,'abstract':abstract,'sameNewsNum':sameNewsNum,'sameNewsUrl':sameNewsNumUrl}
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
    print baiduNews_info("巴拿马")          