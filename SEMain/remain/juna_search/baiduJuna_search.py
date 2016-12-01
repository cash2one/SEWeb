#encoding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")

'''
百度搜索
v1.0
贴吧没有问题
新闻有时候搜的结果内容与界面不一致
新闻获取的图片url在浏览器中访问出现403 forbidden
'''
import time
from lxml import etree
from traceback import format_exc
from urllib2 import urlopen,Request

def baiduSrcTransfor(link):
    res=link.split("/")
    return "https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/"+res[len(res)-1]
def mfReadWebInfo(url='',timeout=300):
    try:
        webInfo = None
        request = Request(url=url)
        #request.add_header('User-Agent',"Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.8.1.6) Gecko/20070914 Firefox/2.0.0.7")
        fd = urlopen(url=request,timeout=timeout)
        webInfo = fd.read().decode('utf-8')
        fd.close()
        return webInfo,None
    except Exception,e:
        print e 
'''
图片是动态加载，暂时没做
'''
def parse_pics(picElement):
    title=picElement.xpath('./h3[contains(@class,"t")]/a')[0].xpath("string(.)").strip()
    titleUrl=picElement.xpath('./h3[contains(@class,"t")]/a')[0].attrib.get('href')
    imgDict={'head':title,'type':'pics','url':titleUrl} #头部信息
    try:  #图片是动态加载
        imgNodes=picElement.xpath('./div[@class="op_img_content"]/div[@id="ala_img_pics"]//a')
        imgUrlList=[]
        if imgNodes is not None and len(imgNodes)>0:
            for imgNode in imgNodes:
                try:
                    imgUrl=imgNode.xpath('./img')[0].attrib.get('src')
                    imgUrlList.append(imgUrl)
                except:
                    pass
        else:
            return None
        imgDict['data']=imgUrlList
    except Exception:
        print format_exc()
        return None
    return imgDict
  
def parse_news_c_border(newsElement):
    newsDict={'type':1,'junaType':'news'}
    dataList=[]
    try:
        c_border=newsElement.xpath('./div[@class="c-border"]')
        if len(c_border)>0:
            try:
                title=c_border[0].xpath('./div/h3[contains(@class,"t")]/a')[0].xpath("string(.)").strip()
                titleUrl=c_border[0].xpath('./div/h3[contains(@class,"t")]/a')[0].attrib.get('href')
                newsDict['head']=title
                newsDict['headUrl']=titleUrl
            except:
                return None
            try: #解析第一个特殊的新闻
                title=c_border[0].xpath('./div/h3[contains(@class,"t")]/a')[0].xpath("string(.)").strip()
                url=c_border[0].xpath('./div/h3[contains(@class,"t")]/a')[0].attrib.get('href')    
                c_row=c_border[0].xpath('./div/div[@class="c-row"]') 
                try:
                    imgUrl=c_row[0].xpath('.//div[contains(@class,"op_sp_realtime_bigpic5_img_con")]')[0].xpath('./a/img')[0].attrib.get('src')
                    if imgUrl is not None:
                        imgUrl=baiduSrcTransfor(imgUrl)   
                except:
                    pass
                abstract=c_row[0].xpath('.//div[@class="op_sp_realtime_bigpic5_first_abs"]')[0].xpath('string(.)').strip()
                where=c_row[0].xpath('.//span[@class="g"]')[0].xpath('string(.)').strip()
                date=c_row[0].xpath('.//span[@class="m"]')[0].xpath('string(.)').strip() 
                firstDict={'type':'news_special','title':title,'abstract':abstract,'imgUrl':imgUrl,'date':date,'where':where,'url':url}
                dataList.append(firstDict)                   
            except:
                pass
            try:
                otherNode=c_border[0].xpath('.//div[@class="op_sp_realtime_bigpic5_list_info"]')[0]
                otherLis=otherNode.xpath('.//div')
                if len(otherLis)>0:
                    for li in otherLis:
                        try:
                            allSpan=li.xpath('.//span')
                            date=allSpan[0].xpath('string(.)').strip()
                            where=allSpan[1].xpath('string(.)').strip()
                            title=li.xpath('./a')[0].xpath('string(.)').strip()
                            url=li.xpath('./a')[0].attrib.get('href')
                            relateNewDict={'type':'news_normal','title':title,'date':date,'where':where,'url':url}
                            dataList.append(relateNewDict)
                        except:
                            pass
            except:
                pass           
    except:
        pass    
    if len(dataList)<=0:  #dataList没有数据则返回None
        return None
    newsDict['data']=dataList
    return newsDict 
      
def parse_news(newsElement): #解析新闻聚纳
    newsDict={'type':1,'junaType':'news'}
    dataList=[]
    try:
        title=newsElement.xpath('./h3[contains(@class,"t")]/a')[0].xpath("string(.)").strip()
        titleUrl=newsElement.xpath('./h3[contains(@class,"t")]/a')[0].attrib.get('href')
        newsDict['head']=title
        newsDict['headUrl']=titleUrl
    except:
        return None
    try:
        first_up=newsElement.xpath('./div[@class="c-offset"]')[0].xpath('./div[@class="c-gap-bottom-small"]')[0]
        firstTitle=first_up.xpath('./a')[0].xpath("string(.)").strip() #第一个相关新闻标题
        firstUrl=first_up.xpath('./a')[0].attrib.get('href') #链接
        first_down=newsElement.xpath('./div[@class="c-offset"]/div[@class="c-row c-gap-bottom-small"]')[0]
        first_imgUrl=first_down.xpath('./a/img[@class="c-img c-img6"]')[0].attrib.get('src') #图片
        if first_imgUrl is not None:
            first_imgUrl=baiduSrcTransfor(first_imgUrl)
        first_abstract=first_down.xpath('./div[@class="c-span-last"]/text()')
        first_abstract=''.join(first_abstract)
        first_dateAndWhere=first_down.xpath('./div[@class="c-span-last"]')[0].xpath(".//span")
        first_where=first_dateAndWhere[0].xpath("string(.)").strip() #来源
        first_date=first_dateAndWhere[1].xpath("string(.)").strip() #时间       
        firstDict={'type':'news_special','title':firstTitle,'abstract':first_abstract,'imgUrl':first_imgUrl,'date':first_date,'where':first_where,'url':firstUrl}
        dataList.append(firstDict)
    except Exception:
        print "parse first news of Baidu error"
    relate_news=newsElement.xpath('./div[@class="c-offset"]/div[@class="c-row"]') #解析其他几个相关新闻
    if relate_news is not None:
        for relate_new in relate_news: #解析单个相关新闻
            try:
                allSpan=relate_new.xpath('./span')
                relateNewTitle=relate_new.xpath('./a')[0].xpath("string(.)").strip() #相关新闻标题
                relateNewUrl=relate_new.xpath('./a')[0].attrib.get('href')
                date=allSpan[0].xpath("string(.)").strip() #相关新闻发布日期
                where=allSpan[1].xpath("string(.)").strip()#相关信息发布网站
                relateNewDict={'type':'news_normal','title':relateNewTitle,'date':date,'where':where,'url':relateNewUrl}
                dataList.append(relateNewDict)
            except Exception:
                print "parse news of Baidu error"
    newsDict['data']=dataList
    if len(dataList)<=0:  #dataList没有数据则返回None
        return None
    return newsDict

def parse_baike(baikeElement): #解析百科
    baikeDict={'type':1,'junaType':'baike'}
    title=None
    titleUrl=None    
    imgUrl=None
    abstract=''
    try:
        title=baikeElement.xpath('./h3/a')[0].xpath("string(.)").strip() #标题
        titleUrl=baikeElement.xpath('./h3/a')[0].attrib.get('href')
        baikeDict['head']=title
        baikeDict['headUrl']=titleUrl        
    except:
        return None
    try:
        imgUrl=baikeElement.xpath('./div[@class="c-row"]/div[@class="c-span6"]')[0].xpath('./a/img[@class="c-img c-img6"]').attrib.get('src')
    except:
        try:
            imgUrl=baikeElement.xpath('.//img[contains(@class,"c-img")]')[0].attrib.get('src')
        except:
            pass
    if imgUrl is not None:
        imgUrl=baiduSrcTransfor(imgUrl)
    try:
        pNodes=baikeElement.xpath('./div[@class="c-row"]/div[@class="c-span18 c-span-last"]')[0].xpath('.//p')
        for i in range(0,len(pNodes)):
            if i>=len(pNodes)-2: #最后两个p不是摘要中的
                break
            abstract=abstract+pNodes[i].xpath('string(.)').strip()
    except:
        pass 
    baikeDict['imgUrl']=imgUrl
    baikeDict['abstract']=abstract 
    return baikeDict 
def parse_tieba(tiebaElement): #解析贴吧
    tiebaDict={'type':1,'junaType':'tieba'}
    dataList=[]
    try:
        try:
            title=tiebaElement.xpath('./h3[contains(@class,"t")]/a')[0].xpath("string(.)").strip()
            titleUrl=tiebaElement.xpath('./h3[contains(@class,"t")]/a')[0].attrib.get('href')
            tiebaDict['head']=title
            tiebaDict['headUrl']=titleUrl 
        except:
            return None    
        tiebaTable=tiebaElement.xpath('./table[@class="op-tieba-general-maintable"]')
        tibaTrs=tiebaTable[0].xpath('.//tr')
        if tibaTrs is not None and len(tibaTrs)>0:
            for tiebaTr in tibaTrs:
                trTdCount=tiebaTr.xpath('.//td') #看该tr下有多少个td标签
                if trTdCount is not None and len(trTdCount)>1: #超过一个则是所需的
                    try:
                        title=tiebaTr.xpath('./td[@class="op-tieba-general-firsttd op-tieba-general-mainpl"]/a')[0].xpath("string(.)").strip() #标题
                        url=tiebaTr.xpath('./td[@class="op-tieba-general-firsttd op-tieba-general-mainpl"]/a')[0].attrib.get('href')
                        click=tiebaTr.xpath('.//td[@class="op-tieba-general-graycolor"]')[0].xpath('./span/i')[0].xpath("string(.)").strip() #点击量
                        reply=tiebaTr.xpath('.//td[@class="op-tieba-general-graycolor"]')[1].xpath('./span/i')[0].xpath("string(.)").strip() #回答数
                        oneDict={'type':'tieba_normal','title':title,'click':click,'reply':reply,'url':url}
                        dataList.append(oneDict)
                    except Exception:
                        print "parse tieba error"
                else:
                    try:
                        imgUrl=tiebaTr.xpath('./td/div[@class="op-tieba-general-mainpic"]/a/img')[0].attrib.get('src')
                        title=tiebaTr.xpath('./td/div[@class="op-tieba-general-main-col op-tieba-general-main-con"]/p[@class="c-gray"]')[0].xpath('string(.)').strip()
                        userNum=tiebaTr.xpath('./td/div[@class="op-tieba-general-main-col op-tieba-general-main-con"]//p')[1].xpath('.//strong')[0].text
                        tieNum=tiebaTr.xpath('./td/div[@class="op-tieba-general-main-col op-tieba-general-main-con"]//p')[2].xpath('.//strong')[0].text
                        oneDict={'type':'tieba_special','title':title,'userNum':userNum,'tieNum':tieNum,'imgUrl':imgUrl}
                        dataList.append(oneDict)
                    except:
                        pass
    except Exception:
        pass
    if len(dataList)<=0:
        return None
    tiebaDict['data']=dataList
    return tiebaDict

#百度搜索相关信息获取
def baidu_relateInfo(webInfo):
    try:
        tree = etree.HTML(webInfo)
        resultList=[]
        main_infos=tree.xpath('/html/body//div[@class="result-op c-container xpath-log"]')
        if main_infos is not None and len(main_infos)>0:
            for main_info in main_infos:
                try:
                    news_info=main_info.xpath('./div[@class="c-offset"]')
                    tieba_info=main_info.xpath('./table[@class="op-tieba-general-maintable"]')
                    if news_info is not None and len(news_info)>0:  #新闻聚纳
                        oneList=parse_news(main_info)
                        if oneList is not None and len(oneList)>0:
                            resultList.append(oneList)
                    if tieba_info is not None and len(tieba_info)>0:  #贴吧聚纳
                        oneList=parse_tieba(main_info)
                        if oneList is not None and len(oneList)>0:
                            resultList.append(oneList)      
                except Exception,e:
                    pass          
        return resultList                         
    except Exception,e:
        print format_exc()
        return None

if __name__ == "__main__":
   webInfo,errorInfo=mfReadWebInfo("http://www.baidu.com/s?wd=习近平",300)
   baidu_relateInfo(webInfo)
