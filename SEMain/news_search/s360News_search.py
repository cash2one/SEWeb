#encoding=utf-8

from urllib2 import urlopen,Request
from lxml import etree
from traceback import format_exc

def readWebInfo(url=None,timeout=300):
    try:
        webInfo = None
        request = Request(url=url)
        #request.add_header('User-Agent',"Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.8.1.6) Gecko/20070914 Firefox/2.0.0.7")
        fd = urlopen(url=request,timeout=timeout)
        webInfo = fd.read().decode('utf-8')
        fd.close()
        return webInfo
    except Exception:
        print format_exc()
        return None

def gets360Url(keyword,page):
    return 'http://news.so.com/ns?q=%s&pn=%s&tn=news&rank=rank&j=0'%(keyword,page)
#根据关键字获取360新闻，page从1开始
def s360News_info(keyword="",page=1):
    url=gets360Url(keyword, page)
    newsText=readWebInfo(url)
    s360NewsSuffix='http://news.so.com/'
    if newsText is None:
        return None
    try:
        resultDict={}
        resultDict['from']='s360'
        resultDict['keyword']=keyword
        resultList=[]
        tree=etree.HTML(newsText)
        resultUl=tree.xpath('/html/body/div[@id="warper"]//ul[@class="result"]')
        if resultUl is not None and len(resultUl)>0:
            lis=resultUl[0].xpath('.//li')
            if lis is not None and len(lis)>0:
                for li in lis: 
                    status=1
                    title=None
                    newsUrl=None
                    imgUrl=None
                    where=None
                    date=None
                    abstract=None
                    sameNewsNum=None
                    sameNewsNumUrl=None
                    tag=None #文章标签                    
                    try:
                        title=li.xpath('./h3/a')[0].xpath('string(.)').strip() #标题
                        newsUrl=li.xpath('./h3/a')[0].attrib.get('href')
                    except:
                        continue
                    newsInfoNode=None
                    try:
                        newsInfoNode=li.xpath('./p[@class="newsinfo"]')[0]
                        where=newsInfoNode.xpath('./span[@class="sitename"]')[0].xpath('string(.)').strip() #来源
                        date=newsInfoNode.xpath('./span[@class="posttime"]')[0].attrib.get('title') #时间
                    except:
                        pass
                    try:
                        newsInfoNode=li.xpath('./p[@class="newsinfo"]')[0]
                        sameNewsNum=newsInfoNode.xpath('./a')[0].xpath('string(.)').strip() #相关新闻数目
                        sameNewsNumUrl=s360NewsSuffix+newsInfoNode.xpath('./a')[0].attrib.get('href')
                    except:
                        pass
                    try:
                        abstract=li.xpath('./p[@class="content"]')[0].xpath('string(.)').strip() #摘要
                    except:
                        pass
                    try: #为了与其他门户网站的新闻格式一致，标签没有加入
                        tagNode=li.xpath('./p[contains(@class,"news_tag")]')[0].xpath('.//a')
                        tagStr=""
                        for aIndex in range(0,len(tagNode)):
                            if aIndex==len(tagNode)-1: #最后一个为'加入讨论'链接
                                break;
                            tagStr=tagStr+tagNode[aIndex].xpath('string(.)').strip()+" "
                        tag=tagStr    
                    except:
                        pass
                    classStr=li.attrib.get('class')
                    if 'hasimg' in classStr: #包含图片的新闻
                        try:
                            imgUrl=li.xpath('./p[@class="pimg"]/a/img')[0].attrib.get('src') #图片
                        except:
                            pass
                    #print 'tag',tag,'title:',title,'newsUrl:',newsUrl,'imgUrl:',imgUrl,'where:',where,'date:',date,'abstract:',abstract,'sameNewsNum:',sameNewsNum,'sameNewsUrl:',sameNewsNumUrl
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
     s360News_info(keyword="习近平",page=1)         