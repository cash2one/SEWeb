#encoding=utf-8

from lxml import etree
from traceback import format_exc
import requests

def readWebInfo(url=None,timeout=300):
    if url is None:
        return None
    try:
        response=requests.get(url=url,timeout=timeout)
        return response.text
    except Exception:
        print format_exc()
        return None

def getSogouUrl(keyword,page):
    return 'http://news.sogou.com/news?mode=1&ie=utf8&query=%s&page=%s'%(keyword,page)
#搜索新闻获取，页面从1开始    
def sogouNews_info(keyword='',page=1):
    url=getSogouUrl(keyword, page)
    newsText=readWebInfo(url=url)
    sogouNewsSuffix='http://news.sogou.com/news'
    if newsText is None:
        return None
    try:
        resultDict={}
        resultDict['from']='sogou'
        resultDict['keyword']=keyword
        resultList=[]
        tree=etree.HTML(newsText)
        allInfoDivs=tree.xpath('/html/body/div[@class="wrap"]/div[@id="wrapper"]/div[@id="main"]/div[@class="results"]//div[@class="vrwrap"]')
        if allInfoDivs is not None and len(allInfoDivs)>0:
            for infoDiv in allInfoDivs:
                title=None
                newsUrl=None
                imgUrl=None
                where=None
                date=None
                abstract=None
                sameNewsNum=None
                sameNewsNumUrl=None                
                try: #如果标题没有获取到则跳过
                    title=infoDiv.xpath('./div/h3[@class="vrTitle"]/a')[0].xpath('string(.)').strip() #标题
                    newsUrl=infoDiv.xpath('./div/h3[@class="vrTitle"]/a')[0].attrib.get('href') #新闻链接
                except:
                    continue
                newsDetailNode=infoDiv.xpath('./div/div[@class="news-detail"]')
                try:
                    imgUrl=newsDetailNode[0].xpath('./a[@class="news-pic"]/img')[0].attrib.get('src') #图片url
                except:
                    pass
                    '''
                    print newsDetailNode[0].xpath('./a[@class="news-pic"]')[0].text
                    imgScriptText=newsDetailNode[0].xpath('./a[@class="news-pic"]/script')
                    print imgScriptText
                    #[0].text
                    imgTextList=imgScriptText.split(';')
                    left=imgTextList[1].find('(')
                    right=imgTextList[1].find(')')
                    imgUrl=imgTextList[left+1:right-1]
                    print imgUrl
                    '''
                try:
                    dateAndWhereStr=newsDetailNode[0].xpath('./div[@class="news-info"]/p[@class="news-from"]')[0].xpath('string(.)').strip()
                    dateAndWhereList=dateAndWhereStr.split()
                    where=dateAndWhereList[0] #来源
                    date=dateAndWhereStr.replace(where,'') #日期
                except:
                    pass
                try:
                    abstract=newsDetailNode[0].xpath('./div[@class="news-info"]/p[@class="news-txt"]/span')[0].xpath('string(.)').strip() #摘要
                except:
                    pass
                try:
                    sameNumsNode=newsDetailNode[0].xpath('./div[@class="news-info"]/p[@class="news-txt"]/a[@id="news_similar"]')
                    sameNewsNum=sameNumsNode[0].xpath('string(.)').strip().replace('>>','')
                    sameNewsNumUrl=sogouNewsSuffix+sameNumsNode[0].attrib.get('href')
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
     sogouNews_info(keyword="巴拿马",page=1)             
