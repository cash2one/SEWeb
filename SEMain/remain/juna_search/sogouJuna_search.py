#encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
'''
搜狗搜索相关聚纳信息
v1.0
新闻和微信聚纳获取不全
'''
import  requests
from lxml import etree
from traceback import format_exc
from urllib2 import urlopen,Request


def mfReadWebInfo2(url='',timeout=300):
    header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
    'Connection':'keep-alive',
    'Cookie':'SUV=1460162941883781; SMYUV=1460162941884122; CXID=17728DC8D9211870D64CA7C46E54E8CB; SUID=445FE29F546C860A570854F8000A8C38; ssuid=6671667376; ABTEST=6|1460945183|v17; pgv_pvi=5393779712; SNUID=AAB10F72EDEBDC070062A005EE2FC5AF; ad=ekllllllll2gjVFclllllVtIXUwlllllXMJKSllllxylllllxVxlw@@@@@@@@@@@; IPLOC=CN1100; JSESSIONID=abc1hBMqJpWphhWAUB7rv; taspeed=taspeedexist; pgv_si=s9957614592; sst0=384; ld=wkllllllll2g3QGSlllllVtILTUlllllXMJKSllllltlllllxllll5@@@@@@@@@@; browerV=3; osV=3; LSTMV=189%2C240; LCLKINT=3093; sct=31',
    'Host':'www.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    }
    try:
        response=requests.get(url,headers=header,timeout=300)
        html=response.text
        return html,None
    except Exception:
        print format_exc()   
    return None,"error"

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

def parseNews(newsElement): #解析新闻
    newsDict={'type':1,'junaType':'news'}
    dataList=[]
    try:
        try:
            headTitle=newsElement.xpath('./h3[@class="vrTitle"]/a')[0].xpath("string(.)").strip() #头部标题 
            headUrl=newsElement.xpath('./h3[@class="vrTitle"]/a')[0].attrib.get('href')
            newsDict['head']=headTitle
            newsDict['headUrl']=headUrl
        except:
            return None
        vrWrapNewsNode=newsElement.xpath('./div[@class="str-pd-box"]')
        try:
            imgUrl=None
            firstNewNode=vrWrapNewsNode[0].xpath('./div[@class="strBox"]/p[@class="str_time"]')[0] #第一个相关信息节点
            firstTitle=firstNewNode.xpath('./a')[0].xpath("string(.)").strip() #标题
            firstUrl=firstNewNode.xpath('./a')[0].attrib.get('href')
            firstDate=None
            abstract='' 
            firstDateNode=firstNewNode.xpath('./span[@class="rt-time"]')
            if firstDateNode is not None and len(firstDateNode)>0:
                firstDate=firstDateNode[0].xpath("string(.)").strip() #时间
            else:
                firstDate=firstNewNode.xpath('string(.)').strip()
            firstWhere=firstNewNode.xpath('./strong')[0].xpath("string(.)").strip() #来源
            try:
                abstract=vrWrapNewsNode[0].xpath('./div[@class="strBox"]/p[@class="str_info"]')[0].xpath('string(.)').strip()
            except:
                pass
            firstDict={'type':'news_special',"title":firstTitle,'abstract':abstract,'imgUrl':imgUrl,'url':firstUrl,"date":firstDate,"where":firstWhere}
            dataList.append(firstDict)
        except Exception:
            pass
        otherNewNodes=None
        try:
            otherNewNodes=vrWrapNewsNode[0].xpath('.//ul[@class="str-ul-list new-ul-list"]')[0].xpath('.//li') #其他相关信息节点
        except:
            pass
        if otherNewNodes is not None:
            for otherNewNode in otherNewNodes:
                try:
                    otherDate=otherNewNode.xpath('./span')[0].xpath("string(.)").strip()
                    otherTitle=otherNewNode.xpath('./a')[0].xpath("string(.)").strip()
                    otherUrl=otherNewNode.xpath('./a')[0].attrib.get('href')
                    otherWhere=otherNewNode.xpath('./strong')[0].xpath("string(.)").strip()
                    otherDict={'type':'news_normal','title':otherTitle,'url':otherUrl,'date':otherDate,'where':otherWhere}
                    dataList.append(otherDict)
                except Exception:
                    print format_exc()
        if len(dataList)<=0:
            return None
        newsDict['data']=dataList
        return newsDict
    except Exception:
        print format_exc()
        return None

def parseBaike(baikeElement): #百科，搜狗百科作为普通条目
    oneDict={}
    title=None
    url=None
    abstract=''
    imgUrl=None
    try:
        title=baikeElement.xpath('./h3/a')[0].xpath("string(.)").strip() #头部标题 
        url=baikeElement.xpath('./h3/a')[0].attrib.get('href')     
    except:
        return None
    try:
        abstractList=baikeElement.xpath('./div[@class="strBox"]//p[@class="str_info"]')
        for one in abstractList:
            abstract=abstract+one.xpath('string(.)').strip()
    except:
        pass
    try:
        imgUrl=baikeElement.xpath('./div[@class="strBox"]/div[@class="str_div"]/a/img')[0].attrib.get('src')
    except:
        pass
    oneDict['title']=title
    oneDict['url']=url
    oneDict['abstract']=abstract
    oneDict['imgUrl']=imgUrl
    return oneDict
def parseWeixin(weixinElement): #解析微信
    weixinDict={'type':1,'junaType':'weixin'}
    dataList=[]
    try:
        headTitle=weixinElement.xpath('./div[@class="vrTitle"]/a')[0].xpath("string(.)").strip() #头部标题 
        headUrl=weixinElement.xpath('./div[@class="vrTitle"]/a')[0].attrib.get('href')
        if headTitle is None or headTitle=="":
            headTitle="相关微信公众号文章"
        weixinDict['head']=headTitle
        weixinDict['headUrl']=headUrl
        firstWXNode=weixinElement.xpath('./div[@class="wx-box-new"]')
        try:
            firstTitle=firstWXNode[0].xpath('./h5[@class="wx-box-h5"]/a')[0].xpath("string(.)").strip() #第一个相关信息标题
            firstUrl=firstWXNode[0].xpath('./h5[@class="wx-box-h5"]/a')[0].attrib.get('href')
            firstDate=None
            try:
                firstDate=firstWXNode[0].xpath('./div/span')[0].xpath("string(.)").strip() #第一个相关信息时间
            except:
                pass
            abstract=''
            try:
                abstract=firstWXNode[0].xpath('./div[@class="div-p2"]//p')[0].xpath('string(.)').strip()
            except:
                pass
            imgUrl=None
            try:
                imgUrl=firstWXNode[0].xpath('./a/img')[0].attrib.get('src')
            except:
                pass
            firstDict={'type':'weixin_special',"title":firstTitle,'abstract':abstract,'imgUrl':imgUrl,'url':firstUrl,"date":firstDate}
            dataList.append(firstDict)
        except Exception:
            pass
        otherWXNodes=firstWXNode[0].xpath('.//ul[@class="wx-list-new"]')[0].xpath('.//li') #其他相关信息节点
        if otherWXNodes is not None:
            for otherWXNode in otherWXNodes:
                otherDate=None
                try:
                    otherDate=otherWXNode.xpath('./p/span[@class="wx-right"]')[0].xpath('string(.)').strip()
                    otherTitle=otherWXNode.xpath('./p/a')[0].xpath("string(.)").strip()
                    otherUrl=otherWXNode.xpath('./p/a')[0].attrib.get('href')
                    otherDict={'type':'weixin_normal','title':otherTitle,'url':otherUrl,'date':otherDate}
                    dataList.append(otherDict)
                except Exception:
                    print format_exc()
        if len(dataList)<=0:
            return None
        weixinDict['data']=dataList
        return weixinDict
    except Exception:
        print format_exc()
        return None
#搜狗搜索
def sogou_relateInfo(webInfo):
    try:
        tree = etree.HTML(webInfo)
        resultList=[]
        vrWrapNodes=tree.xpath('/html/body//div[@class="vrwrap"]') #获取所有聚合信息节点
        #print 'vrWrapNodes',vrWrapNodes
        if vrWrapNodes is not None:
            for vrWrapNode in vrWrapNodes:
                try:
                    vrWrapNewsNode=vrWrapNode.xpath('.//div[@class="str-pd-box"]')
                    vrWrapWXNode=vrWrapNode.xpath('.//div[@class="wx-box-new"]')
                    #print 'vrWrapNewsNode',vrWrapNewsNode
                    if vrWrapNewsNode is not None and len(vrWrapNewsNode)>0: #新闻相关聚纳存在 
                        oneList=parseNews(vrWrapNode)
                        if oneList is not None and len(oneList)>0:
                            resultList.append(oneList)  
                    #print 'vrWrapWXNode',vrWrapWXNode
                    if vrWrapWXNode is not None and len(vrWrapWXNode)>0: #微信相关聚纳存在 
                        oneList=parseWeixin(vrWrapNode)  
                        if oneList is not None and len(oneList)>0:
                            resultList.append(oneList)                        
                except Exception:
                    print format_exc() 
        return resultList  
    except Exception:
        print format_exc()
        return None

if __name__ == "__main__":
   webInfo,errorInfo=mfReadWebInfo2("http://www.sogou.com/web?query=李克强",300)
   sogou_relateInfo(webInfo)


