#encoding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")
'''
bin搜索相关聚纳信息
v1.0 使用 selenium加载js

新闻获取不全
'''
from traceback import format_exc
from urllib2 import urlopen,Request


def mfReadWebInfo(url='',timeout=300):
    try:
        webInfo = None
        request = Request(url=url)
        #request.add_header('User-Agent',"Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.8.1.6) Gecko/20070914 Firefox/2.0.0.7")
        fd = urlopen(url=request,timeout=timeout)
        webInfo = fd.read().decode('utf-8')
        fd.close()
        return webInfo,None
    except Exception:
        print format_exc()
    
def parseNewsWithoutSelenium(newsElement): #不使用selenium解析新闻聚纳
    try:
        newsDict={'type':1,'junaType':'news'}
        dataList=[]
        ans_news=newsElement.xpath('./div[@id="ans_news"]/div[@id="snct"]')
        if ans_news is not None and len(ans_news)>0:
            headTitle=ans_news[0].xpath('./h2')[0].xpath('string(.)').strip() # 头部标题
            newsDict['head']=headTitle
            newsDict['headUrl']=None   #bing的新闻聚纳头部标题不是链接      
            try:
                otherNewsNodes=ans_news[0].xpath('./div[@class="b_rich"]/div[contains(@class,"mcd")]')
                if otherNewsNodes is not None and len(otherNewsNodes)>0:
                    for otherNews in otherNewsNodes:
                        try:
                            imgUrl=None
                            date=None
                            title=None
                            url=None
                            where=None
                            abstract=''
                            try: #图片,有点问题
                                '''
                                otherNewImgUrl=otherNews.xpath('./div[@class="b_clearfix b_overflow"]/div[@class="b_float_img"]//img')[0].attrib.get('src')
                                if otherNewImgUrl is not None:
                                    imgUrl=otherNewImgUrl
                                else:
                                    try:
                                        otherNewImgUrl=otherNews.xpath('.//div[@class="b_float_img"]')[0].xpath('.//img')[0].attrib.get('src')
                                    except:
                                        pass
                                '''
                                pass
                            except:
                                pass
                            otherNodeInfoNode=otherNews.xpath('./div[@class="b_clearfix b_overflow"]/div[@class="b_overflow"]')
                            if otherNodeInfoNode is not None and len(otherNodeInfoNode)>0:
                                try:
                                    title=otherNodeInfoNode[0].xpath('./h4/a')[0].xpath('string(.)').strip()
                                    url=otherNodeInfoNode[0].xpath('./h4/a')[0].attrib.get('href')
                                    date=otherNodeInfoNode[0].xpath('./div[@class="b_attribution"]/cite/span')[0].xpath('string(.)').strip()
                                    where=otherNodeInfoNode[0].xpath('./div[@class="b_attribution"]/cite')[0].xpath('string(.)').strip()
                                    where=where.replace(date,'')
                                    date=date.replace('·','')
                                except:
                                    pass
                                try:
                                    abstract=otherNews.xpath('.//p[@class="snippet"]')[0].xpath('string(.)').strip()
                                except:
                                    pass
                            else:
                                try:
                                    title=otherNews.xpath('./h4/a')[0].xpath('string(.)').strip()
                                    url=otherNews.xpath('./h4/a')[0].attrib.get('href')
                                    try:
                                        date=otherNews.xpath('./div[@class="b_attribution"]/cite/span[@class="b_secondaryText"]')[0].xpath('string(.)').strip()
                                        where=otherNews.xpath('./div[@class="b_attribution"]/cite')[0].xpath('string(.)').strip()
                                        where=where.replace(date,'')
                                        date=date.replace('·','')   
                                    except:
                                        pass 
                                    try:
                                        abstract=otherNews.xpath('.//p[@class="snippet"]')[0].xpath('string(.)').strip()
                                    except:
                                        pass                                                                 
                                except:
                                    pass                                 
                            otherDict={'type':'news_special','title':title,'abstract':abstract,'imgUrl':imgUrl,'date':date,'where':where,'url':url}
                            dataList.append(otherDict)
                        except Exception:
                            pass
            except Exception:
                print format_exc()  
        else:
            return None
        newsDict['data']=dataList                
        return newsDict
    except Exception:
        print format_exc()
        return None

#bing搜索
def bing_relateInfo(url):   
    pass

if __name__ == "__main__":
    bing_relateInfo('https://www.bing.com/search?q=习近平')

