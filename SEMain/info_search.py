# encoding: utf-8

import base64
import multiprocessing
import thread
import threading
import time
import json
from lxml import etree
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import gevent
import requests
from gevent import monkey
from json import JSONEncoder
import re
import sys


from traceback import format_exc
from mutex import mutex
from news_search import baiduNews_search,sogouNews_search,s360News_search,chinaNews_search

reload(sys)
sys.setdefaultencoding('utf8')

# 将list切分成n个list
def div_list(ls,n):
    if not isinstance(ls,list) or not isinstance(n,int):
        return []
    ls_len = len(ls)
    if n<=0 or 0==ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = ls_len/n
        k = ls_len%n
        ls_return = []
        for i in xrange(0, (n-1)*j, j):
            ls_return.append(ls[i:i+j])
        ls_return.append(ls[(n-1)*j:])
        return ls_return

# 百度搜索引擎爬虫,page从1开始
def baidu_search(word ,page,delay=False):
    if(delay):# 多线程请求时设置延时，防止网络拥塞及IP被BAN
        time.sleep(0.1*page)    
    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection':'keep-alive',
        'Host':'www.baidu.com',
        'Cookie':'BAIDUID=F31C164C35C9456902BD2E82DED62027:FG=1; PSTM=1459240026; BIDUPSID=A374184AC82E6781BC2986BFC8CBE674; BDSFRCVID=j9LsJeC62CKYBy5RsXUyb4JDnKzhvP3TH6aoi6G_szxX7i3b8ielEG0PJ7lQpYD-hILjogKK0mOTHvbP; H_BDCLCKID_SF=tJPtoCt2JIvSDn4kKJL_-P4DenQieRJZ5mAqot0-34cxHU_GWl5j-60m0UTLq4RftgOnaIQqWR0MfpvgyUjZ3U_BX4-jBho43bRT0DOsL4JZs56N-lQphP-UyN3LWh37bDrTVDKhJDtbMC_r247Eb-_eqx5Ka43tHD7yWCvgMIb5OR5JLtQV3ptTDM6N5fnKbmcHWhO15hvvhb3O3MA-yUKWjJ7U5xoXyGceoUQF545zSlux0bOchh_QWt8LJPnCKDOMahkM5h7xOKLG05CBj6vBDHAsaPRJ5CtXQ458K4__Hn7zepQCXbtpbt-qJt7wQ5TIWfobKxbos4ovLUvJyTL0KxbnBT5Ka5IeBJjy-pbmEl5oQqnK2R8kQN3T-URQL6RkKTCyyx3kDn3oyT3VXp0n5x5Tqj_ffR4f_CLQb-3bK4jnh-nhbKCShUFsabOT-2Q-5hOy3KOCol4G0RbDylKm5PTl5jJPQ6TUa43g-pu-hpFuDjtBD5b0jGRf-b-X-C7QW-5eHJOoDDvdqfr5y4LdLp7xJhjzBnTNQh6uyDoqMtJm5lol5q-P5POjWjKeWJLq_KPKtDK5bnO1MtbOq4_jMqrt2D62aKDs2q3o-hcqEpO9QTbS0-Fp0lbuhU3rJRbEMMJ7HlcfjlbVLxt5DUThjNK8J5KJtR3fL-08-ROSDP5gq4bohjPIbJ3eBtQmJJu8Wb5X3UjCqp6z3bJFhbbWhJJU3l-qQg-q3lTkXKb-b-bD56oT3htLyxCO0x-jLgQ9WUjMyl-VOnRX3tnJyUnQhtnnBn5aLnLf_IP2fC0MbP365IT85tk8qxbXq-I8BT7Z0l8KtqOvoqowjq55WhL--GOZ0P6iMDbqbIOmWIQHDnICQpn52RkRjUue5jv05CJ4KKJxWD3SVtJXQKcsyfAqhUJiB5OLBan7LJoxfJOKHIClj58beM5; BDUSS=FvMXVKUW4tVXRxSW9-eVNubUIxLU5-T3V6RFRGd0l6cEdvVFBidTM3NGEwWEZYQVFBQUFBJCQAAAAAAAAAAAEAAAArxB0S0sDIu86qxONfRmx5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABpESlcaREpXeU; ispeed_lsm=0; BDRCVFR[IoBQEhO7fdb]=mk3SLVN4HKm; BD_CK_SAM=1; H_PS_PSSID=; BD_UPN=12314353; sugstore=0; H_PS_645EC=9d68y2N4C0CTOH7YCRGTI4vCIA1v6KAhwuku29Cb9ttvPNNCXW%2FwVAjTdANp1AsZhlFW13GX',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'     
    }
    url='https://www.baidu.com/s?wd='+word+'&pn='+str(10*(page-1))
    #print '正在搜索百度搜索...'
    try:
        response=requests.get(url=url,headers=header)
    except:
        print format_exc()
        return None
    tree = etree.HTML(response.text)
    searchInfo={'keyword':word,'browser':'baidu','status':-2}  # status -2表示其他异常
    if ('抱歉' in response.text or '很抱歉' in response.text or '对不起' in response.text) and ('未找到' in response.text or '没有找到' in response.text):
        searchInfo['status']=0  #status=0表明没有找到对应网页
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'
    resultList=[]
    main_infos=tree.xpath('/html/body//div[contains(@class,"c-container")]')
    if main_infos is not None and len(main_infos)>0:
        for element in main_infos:
            classStr=element.attrib.get('tpl')
            imgUrl=None
            title=None
            url=None
            abstract=''
            if classStr=='se_com_default': #普通节点
                try:
                    title=element.xpath('./h3/a')[0].xpath('string(.)').strip() #标题
                    url=element.xpath('./h3/a')[0].attrib.get('href') #链接
                except:
                    pass
                try:
                    abstract=element.xpath('.//div[contains(@class,"c-abstract")]')[0].xpath('string(.)').strip()
                except:
                    pass
                if abstract is None or abstract=='' or len(abstract)==0:   
                    detailsNode=element.xpath('./div[@class="c-row c-gap-top-small"]')
                    try:
                        abstract=detailsNode[0].xpath('.//div[contains(@class,"c-abstract")]')[0].xpath('string(.)').strip()
                    except:
                        pass
                    try:
                        imgUrl=detailsNode[0].xpath('./div[contains(@class,"general_image_pic")]')[0].xpath('./a/img').attrib.get('src')
                    except:
                        try:
                            imgUrl=detailsNode[0].xpath('.//img[contains(@class,"c-img")]')[0].attrib.get('src')
                        except:
                            pass
                normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict)
            elif classStr=="bk_polysemy": #百科
                try:
                    oneDict=baiduJuna_search.parse_baike(element)
                    if oneDict is not None and len(oneDict)>0:
                        resultList.append(oneDict)
                except:
                    pass
            elif classStr=="sp_img": #图片集纳
                try:
                    continue
                    #图片是动态加载，暂时没有做
                    oneDict=baiduJuna_search.parse_pics(element)
                    if oneDict is not None and len(oneDict)>0:
                        resultList.append(oneDict)
                except:
                    pass
            elif classStr=="sp_realtime_bigpic5": #新闻集纳
                try: #新闻集纳有两种样式
                    c_offset=element.xpath('.//div[@class="c-offset"]')
                    c_border=element.xpath('.//div[@class="c-border"]')
                    oneDict=None
                    if c_offset is not None and len(c_offset)>0:
                        oneDict=baiduJuna_search.parse_news(element)
                    elif c_border is not None and len(c_border)>0:
                        oneDict=baiduJuna_search.parse_news_c_border(element)
                    if oneDict is not None and len(oneDict)>0:
                        resultList.append(oneDict)
                except:
                    pass
            elif classStr=="tieba_general": #贴吧
                try:
                    oneDict=baiduJuna_search.parse_tieba(element)
                    if oneDict is not None and len(oneDict)>0:
                        resultList.append(oneDict)
                except:
                    pass
            elif classStr=="url":
                try:
                    title=element.xpath('./h3//a')[0].xpath('string(.)').strip() #标题
                    url=element.xpath('./h3//a')[0].attrib.get('href')
                except:
                    continue
                try:
                    abstract=element.xpath('./div[@class="op_url_size c-row"]')[0].xpath('string(.)').strip() #摘要
                except:
                    pass
                normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict)
            elif classStr=="vd_mininewest": #视频聚纳
                try:
                    title=element.xpath('./h3//a')[0].xpath('string(.)').strip() #标题
                    url=element.xpath('./h3//a')[0].attrib.get('href')
                except:
                    continue
                try:
                    abstract=element.xpath('./div[@class="c-row"]')[0].xpath('string(.)').strip() #摘要
                except:
                    pass
                normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict) 
            elif classStr=='ecl_temai_classic_senior': #特卖
                try:
                    title=element.xpath('./h4//a')[0].xpath('string(.)').strip() #标题
                    url=element.xpath('./h4//a')[0].attrib.get('href')
                except:
                    continue
                try:
                    abstract=element.xpath('.//div[@class="c-row"]')[0].xpath('string(.)').strip() #摘要
                except:
                    pass
                normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict)                                
            elif classStr=="shares_simple": #股市行情
                try:
                    title=element.xpath('./h3//a')[0].xpath('string(.)').strip() #标题
                    url=element.xpath('./h3//a')[0].attrib.get('href')
                except:
                    continue
                try:
                    abstract=element.xpath('./div[@class="op_shares_simple"]')[0].xpath('string(.)').strip() #摘要
                except:
                    pass
                normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict)  
            elif classStr=="singlevideo":
                try:
                    title=element.xpath('./h3//a')[0].xpath('string(.)').strip() #标题
                    url=element.xpath('./h3//a')[0].attrib.get('href')
                except:
                    continue
                try:
                    abstract=element.xpath('./div[@class="c-row"]/div[contains(@class,"c-span18")]')[0].xpath('string(.)').strip() #摘要
                except:
                    pass
                try:
                    imgUrl=element.xpath('./div[@class="c-row"]/div[@class="c-span6"]/a/img')[0].attrib.get('src')
                except:
                    pass
                normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict)  
            elif classStr=="generaltable":
                try:
                    title=element.xpath('./h3//a')[0].xpath('string(.)').strip() #标题
                    url=element.xpath('./h3//a')[0].attrib.get('href')
                except:
                    continue
                try:
                    abstract=element.xpath('.//div[@class="c-border"]')[0].xpath('string(.)').strip() #摘要
                except:
                    pass
                normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict) 
    if len(resultList)<=0:
        searchInfo['data']=None
    else:
        searchInfo['status']=1  #status为1表明成功                                             
        searchInfo['data']=resultList 
    if searchInfo['status']==-2:
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'        
    #print '百度搜索搜索完毕...'  
    
    mutex.acquire()
    data_list.append(searchInfo)
    mutex.release()

    return searchInfo

#360搜索引擎爬虫，页面从1开始
def s360_search (word ,page,delay=False):
    if(delay):
        time.sleep(0.1*page)
    header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Host':'www.so.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36 '   
    }
    url='https://www.so.com/s?q='+word+'&pn='+str(page)
    #print '正在搜索360搜索...'
    try:
        response=requests.get(url=url,headers=header)
    except:
        print format_exc()
        return None  
    tree = etree.HTML(response.text.encode(response.encoding).decode('utf-8')) 
    searchInfo={'keyword':word,'browser':'360','status':-2} #status为-2表明其他异常
    resultList=[]
    noResultNode=tree.xpath('/html/body//div[@id="no-result"]')
    if noResultNode is not None and len(noResultNode)>0:
        searchInfo['status']=0
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'
    main_info=tree.xpath('/html/body//li[@class="res-list"]')
    if main_info is not None and len(main_info)>0:
        for element in main_info:
            baikeNode=element.xpath('./div[@class="res-rich res-baike clearfix"]') #百科聚纳
            junaPicNode=element.xpath('./div[@id="mohe-360pic"]') #图片聚纳
            junaNewNode=element.xpath('./div[@id="mohe-news"]') #新闻聚纳
            junaZhihuNode=element.xpath('./div[@id="mohe-biu_zhihu"]') #知乎聚纳
            if baikeNode is not None and len(baikeNode)>0: #百科
                try:
                    oneDict=s360Juna_search.parseBaike(element)
                    if oneDict is not None and len(oneDict)>0:
                        resultList.append(oneDict)                    
                except:
                    pass
            elif junaPicNode is not None and len(junaPicNode)>0: #图片
                pass
            elif junaNewNode is not None and len(junaNewNode)>0: #新闻
                try:
                    oneDict=s360Juna_search.parseNews(element)
                    if oneDict is not None and len(oneDict)>0:
                        resultList.append(oneDict)
                except:
                    pass
            elif junaZhihuNode is not None and len(junaZhihuNode)>0: #知乎
                try:
                    oneDict=s360Juna_search.parseZhihu(element)
                    if oneDict is not None and len(oneDict)>0:
                        resultList.append(oneDict)
                except:
                    pass
            else: #普通节点
                title=None
                url=None
                imgUrl=None
                abstract=''
                try:
                    try:
                        title=element.xpath('./h3[@class="res-title "]/a')[0].xpath('string(.)').strip() #标题
                        url=element.xpath('./h3[@class="res-title "]/a')[0].attrib.get('href') #链接
                    except:
                        try:
                            title=element.xpath('./h3[@class="res-title"]/a')[0].xpath('string(.)').strip() #标题
                            url=element.xpath('./h3[@class="res-title"]/a')[0].attrib.get('href') #链接
                        except:
                            continue
                    try:
                        abstract=element.xpath('.//p[@class="res-desc"]')[0].xpath('string(.)').strip()
                    except:
                        try:
                            abstract=element.xpath('./div[contains(@class,"res-rich")]/div')[0].xpath('string(.)').strip()
                        except:
                            try:
                                abstract=element.xpath('./div[contains(@class,"res-rich")]/div[@class="res-comm-con"]')[0].xpath('string(.)').strip()
                            except:
                                try:
                                    abstract=element.xpath('./div[contains(@class,"res-rich")]')[0].xpath('string(.)').strip()
                                except:
                                    try:
                                        abstract=element.xpath('.//div[contains(@class,"res-desc")]')[0].xpath('string(.)').strip()
                                    except:
                                        pass                               
                    normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                    normalDict={'type':0,'data':normalData}
                    resultList.append(normalDict)
                except:
                    pass
    if len(resultList)<=0:
        searchInfo['data']=None
    else:
        searchInfo['status']=1  #status 为1表明成功
        searchInfo['data']=resultList
    if searchInfo['status']==-2:
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'        
    #print '360搜索搜索完毕...' 
    
    mutex.acquire()
    data_list.append(searchInfo)
    mutex.release()    
    
    return searchInfo
#搜狗搜索
def sogou_search (word ,page,delay=False):
    if(delay):
        time.sleep(0.2*page)
    url='http://www.sogou.com/web?query='+word+'&ie=utf8&page='+str(page)
    # 设置请求header,防止被ban,可在浏览器中提取
    headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
        'Host':'www.sogou.com',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    }
    #print  '正在搜索搜狗搜索...'
    try:
        response=requests.get(url=url, headers=headers)
    except Exception:
        print format_exc()
        return None
    html = response.text
    tree = etree.HTML(html)
    searchInfo={'keyword':word,'browser':'sogou','status':-2} #status为-2表示其他异常
    resultList=[]   
    main_info=tree.xpath('/html/body/div[@class="wrap"]/div[@class="wrapper"]/div[@class="main"]')
    vrwraps=main_info[0].xpath('.//div[@class="vrwrap"]') #聚纳
    rbs=main_info[0].xpath('.//div[@class="rb"]') #普通
    vrPic=main_info[0].xpath('.//div[contains(@class,"vrPic")]') #图片聚纳
    if rbs is not None and len(rbs)>0: #普通
        for rb in rbs:
            title=None
            url=None
            abstract=''
            imgUrl=None
            try:
                try:
                    title=rb.xpath('./h3/a')[0].xpath('string(.)').strip() #标题
                    url=rb.xpath('./h3/a')[0].attrib.get('href') #链接
                except:
                    continue
                try:
                    abstract=rb.xpath('.//div[@class="ft"]')[0].xpath('string(.)').strip()
                except:
                    try:
                        abstract=rb.xpath('.//table')[0].xpath('string(.)').strip()
                    except:
                        pass
                normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict)            
            except Exception:
                pass 
    if vrPic is not None and len(vrPic)>0: #图片聚纳
        pass
    if vrwraps is not None and len(vrwraps):
        for vrwrap in vrwraps:
            try:
                vrWrapNewsNode=vrwrap.xpath('.//div[@class="str-pd-box"]')
                vrWrapWXNode=vrwrap.xpath('.//div[@class="wx-box-new"]')
                vrStrBox=vrwrap.xpath('.//div[@class="strBox"]')
                if vrWrapNewsNode is not None and len(vrWrapNewsNode)>0: #新闻相关聚纳存在 
                    try:
                        oneDict=sogouJuna_search.parseNews(vrwrap)
                        if oneDict is not None and len(oneDict)>0:
                            resultList.append(oneDict)  
                    except:
                        pass
                elif vrWrapWXNode is not None and len(vrWrapWXNode)>0: #微信相关聚纳存在 
                    try:
                        oneDict=sogouJuna_search.parseWeixin(vrwrap)  
                        if oneDict is not None and len(oneDict)>0:
                            resultList.append(oneDict) 
                    except:
                        pass 
                elif vrStrBox is not None and len(vrStrBox)>0: #搜狗的百科作为普通条目          
                    try:  
                        oneDict=sogouJuna_search.parseBaike(vrwrap)                          
                        if oneDict is not None:
                            normalDict={'type':0,'data':oneDict}
                            resultList.append(normalDict) 
                    except:
                        pass                                
            except Exception:
                print format_exc() 
    if len(resultList)<=0:
        searchInfo['data']=None
    else:
        searchInfo['status']=1  #status为1表明成功                                             
        searchInfo['data']=resultList
    if searchInfo['status']==-2:
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'
    #print '搜狗搜索搜索完毕...'           
    mutex.acquire()
    data_list.append(searchInfo)
    mutex.release()    
    return searchInfo

#中国搜索,page从1开始
def china_search(word,page,delay=False):
    if(delay):
        time.sleep(0.2*page)
    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
        'Connection':'keep-alive',
        'Host':'www.chinaso.com',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }
    url='http://www.chinaso.com/search/pagesearch.htm?q='+word+'&page='+str(page)+'&wd='+word 
    #print '正在搜索中国搜索...'   
    try:
        response=requests.get(url=url,headers=header)
    except:
        print format_exc()
        return None
    tree=etree.HTML(response.text)
    
    responseText=open('1.html','w')
    responseText.write(response.text)
    responseText.close()
    searchInfo={'keyword':word,'browser':'china','status':-2}
    if u'访问出现异常' in response.text and '验证码' in response.text:
        print '***********中国搜索访问出现异常*************'
        searchInfo['status']=-1 #status为-1表明被封
        searchInfo['description']=url
    resultList=[]
    chinaSuffix='http://www.chinaso.com'
    main_infos=tree.xpath('/html/body/div[@class="mainWrapper clearfix"]/div[@class="resultWrapper fl"]//li[@class="reItem "]')    
    if main_infos is not None and len(main_infos)>0:
        for info in main_infos:
            title=None
            titleUrl=None
            abstract=''
            imgUrls=[]
            baikeBox=info.xpath('.//div[contains(@class,"baikeBox")]') #百科
            lunabox_news=info.xpath('.//div[@id="lunabox_news"]') #新闻集纳
            newsPicListB=info.xpath('.//div[contains(@class,"newsPicListB")]') #带多个图片的新闻
            normal=info.xpath('./div[@class="reNewsWrapper clearfix"]') #普通新闻
            boxImageleftA=info.xpath('.//div[@id="boxImageleftA"]') #国搜图片
            reVideoList=info.xpath('.//ul[contains(@class,"reVideoList")]') #国搜视频
            boxAQLeftA=info.xpath('.//div[@id="boxAQLeftA"]') #国搜问答           
            if len(baikeBox)>0 or len(normal)>0: #百科和普通的规则差不多
                try:
                    title=info.xpath('./h2/a')[0].xpath('string(.)').strip() #标题
                    titleUrl=chinaSuffix+info.xpath('./h2/a')[0].attrib.get('href')
                except:
                    continue
                try: #图片
                    imgUrl=info.xpath('.//div[@class="reNewsImgWrapper fl"]')[0].xpath('./div[@class="imgVM"]/a')[0].xpath('.//img')[0].attrib.get('src')
                    if len(imgUrl)>0:
                        imgUrls.append(imgUrl)
                except:
                    try:
                        imgUrl=info.xpath('.//div[@class="imgVM"]')[0].xpath('./a/span/img')[0].attrib.get('src')
                        if len(imgUrl)>0:
                            imgUrls.append(imgUrl)
                    except:
                        pass
                try: #摘要
                    abstract=info.xpath('.//div[@class="reNewsContL fr"]')[0].xpath('.//p')[0].xpath('string(.)').strip()
                except:
                    try:
                        abstract=info.xpath('./div[@class="reNewsWrapper clearfix"]/div//p')[0].xpath('string(.)').strip()
                    except:
                        pass
                normalData={'title':title,'url':titleUrl,'abstract':abstract,'imgUrls':imgUrls}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict) 
            if len(lunabox_news)>0: #新闻集纳
                continue
            elif len(newsPicListB)>0: #带多个图的新闻
                try:
                    title=info.xpath('./h2/a')[0].xpath('string(.)').strip() #标题
                    titleUrl=chinaSuffix+info.xpath('./h2/a')[0].attrib.get('href')
                except:
                    continue
                try:
                    abstract=info.xpath('./p')[0].xpath('string(.)').strip() #摘要
                except:
                    pass
                try:
                    liNodes=info.xpath('./div[@class="clearfix newsPicListB por"]/ul[@class="newsPicListBCon"]//li')
                    for li in liNodes:
                        imgUrl=li.xpath('./a/img')[0].attrib.get('src')
                        if len(imgUrl)>0:
                            imgUrls.append(imgUrl)
                except:
                    pass
                normalData={'title':title,'url':titleUrl,'abstract':abstract,'imgUrls':imgUrls}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict) 
            elif len(boxImageleftA)>0: #国搜图片
                try:
                    title=info.xpath('./div[@class="boxImageleftA"]/h2/a')[0].xpath('string(.)').strip() #标题
                    titleUrl=chinaSuffix+info.xpath('./div[@class="boxImageleftA"]/h2/a')[0].attrib.get('href')
                except:
                    continue    
                try:
                    liNodes=info.xpath('./div[@class="boxImageleftA"]/ul//li')
                    for li in liNodes:
                        imgUrl=li.xpath('./a/img')[0].attrib.get('src')
                        if len(imgUrl)>0:
                            imgUrls.append(imgUrl)
                except:
                    pass    
                normalData={'title':title,'url':titleUrl,'abstract':abstract,'imgUrls':imgUrls}
                normalDict={'type':0,'data':normalData}
                resultList.append(normalDict)         
            elif len(reVideoList)>0:
                continue
            elif len(boxAQLeftA)>0: #问答集纳
                continue
            else:
                continue
        if page==1:           
            lunaNewsDict=chinaJuna2_search.parseNews(word) #新闻集纳
            if lunaNewsDict is not None:
                resultList.append(lunaNewsDict)
            lunaWendaDict=chinaJuna2_search.parseWenDa(word) #问答集纳
            if lunaWendaDict is not None:
                resultList.append(lunaWendaDict)
    if len(resultList)<=0:
        searchInfo['data']=None
    else:
        searchInfo['status']=1  #status为1表明成功                                             
        searchInfo['data']=resultList  
    if searchInfo['status']==-2:
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'        
    #print '中国搜索搜索完毕...'  
    
    mutex.acquire()
    data_list.append(searchInfo)
    mutex.release()
    
    return searchInfo            

#微软bing搜索
def getBingCVID():
    url = "http://cn.bing.com/"
    try:
        response = requests.get(url,timeout=3)
        html_text = response.text
        try:
            m= re.search("IG:\"(.*)\",EventID:",html_text)
            if m:
                IG= m.group(1)
                return IG
        except Exception as e:
            print(e)
    except:
        print "Get Bing cvid error"
    return None
def bing_search(word ,page,delay=False):
    if(delay):
        time.sleep(0.1*page)
    header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection':'keep-alive',
            'Host':'cn.bing.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    }
    #print '正在搜索 Bing搜索...'
    cvid=getBingCVID()
    if cvid is None:
        return None
    if page<=1:
        page=1
    else:
        page=(page-1)*10
    main_url='https://www.bing.com/search?q='+word+'&first='+str(page)+'&cvid='+cvid+'&FORM=PERE'
    response=None
    try:
        response=requests.get(main_url,headers=header,timeout=300)
    except Exception:
        print format_exc()
        return None
    html=response.text
    tree = etree.HTML(html)
    searchInfo={'keyword':word,'browser':'bing','status':-2}
    resultList=[]     
    main_info=tree.xpath('/html/body/div[@id="b_content"]/ol[@id="b_results"]')
    if main_info is not None and len(main_info)>0:
        b_algoes=main_info[0].xpath('.//li[contains(@class,"b_algo")]') #普通
        b_ans=main_info[0].xpath('.//li[contains(@class,"b_ans")]') #聚纳
        if b_algoes is not None and len(b_algoes)>0:
            for b_algo in b_algoes:
                imgUrl=None
                try:
                    title=None
                    url=None
                    try:
                        title=b_algo.xpath('./h2/a')[0].xpath('string(.)').strip() #标题
                        url=b_algo.xpath('./h2/a')[0].attrib.get('href') #链接
                    except:
                        try:
                            title=b_algo.xpath('./div[@class="b_title"]/h2/a')[0].xpath('string(.)').strip() #标题
                            url=b_algo.xpath('./div[@class="b_title"]/h2/a')[0].attrib.get('href') #链接
                        except:
                            continue
                    abstract=''
                    try:
                        abstract=b_algo.xpath('./div[@class="b_caption"]/p')[0].xpath('string(.)').strip() #摘要
                    except:
                        try:
                            abstract=b_algo.xpath('.//p')[0].xpath('string(.)').strip() #摘要
                        except:
                            pass
                    normalData={'title':title,'url':url,'abstract':abstract,'imgUrl':imgUrl}
                    normalDict={'type':0,'data':normalData}
                    resultList.append(normalDict)            
                except Exception:
                    print format_exc()
        if b_ans is not None and len(b_ans)>0:
            for b_an in b_ans:
                try:
                    newsJuna=b_an.xpath('.//div[@id="ans_news"]')
                    if newsJuna is not None and len(newsJuna)>0: #解析新闻聚纳
                        oneDict=bingJuna_search.parseNewsWithoutSelenium(b_an)
                        if oneDict is not None and len(oneDict)>0:
                            resultList.append(oneDict) 
                except Exception:
                    pass
    if len(resultList)<=0:
        searchInfo['data']=None
    else:
        searchInfo['status']=1  #status为1表明成功                                             
        searchInfo['data']=resultList
    if searchInfo['status']==-2:
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'
    #print 'Bing搜索搜索完毕...'           
    mutex.acquire()
    data_list.append(searchInfo)
    mutex.release()
    return searchInfo    

#神马搜索,page从1开始
def shen_ma_search(word ,page,delay=False):
    if(delay):
        time.sleep(0.2*page)
    # 神马搜索页面URL需要进行BASE64编码转换
    base64_text = base64.encodestring(word).strip()
    base64_text=base64_text.replace('+','!') #神马搜索会把编码后的文字中的'+'换成'!'
    if(page==1):
        url=u'http://aibing.cc/shenma/'+base64_text+u'.html'
    else:
        url=u'http://aibing.cc/shenma/'+base64_text+'_'+str(page)+u'.html'
    #print '正在搜索神马搜索...'
    try:
        response=requests.get(url=url)
    except Exception:
        print format_exc()
        return None
    tree = etree.HTML(response.text)
    searchInfo={'keyword':word,'browser':'shenma','status':-2}
    if ('抱歉' in response.text or '很抱歉' in response.text or '对不起' in response.text) and ('未找到' in response.text or '没有找到' in response.text):
        searchInfo['status']=0  #status=0表明没有找到对应网页
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'
    resultList=[]
    urlSuffix="http://aibing.cc"
    main_infoLi=tree.xpath('/html/body//div[@class="g"]')
    if main_infoLi is not None and len(main_infoLi)>0:
        for g in main_infoLi:
            try:
                title=g.xpath('./h2/a')[0].xpath('string(.)').strip() #标题
                url=urlSuffix+g.xpath('./h2/a')[0].attrib.get('href') #链接
                abstract=g.xpath('./div[@class="std"]')[0].xpath('string(.)').strip() #摘要
                data={'title':title,'url':url,'abstract':abstract}
                gData={'type':0,'data':data}
                resultList.append(gData)
            except Exception:
                pass
    if len(resultList)<=0:
        searchInfo['data']=None
    else:
        searchInfo['status']=1  #status为1表明成功                                             
        searchInfo['data']=resultList 
    if searchInfo['status']==-2:
        searchInfo['description']='抱歉，您查找的关于  '+word+' 的页面不存在'
    #print '神马搜索搜索完毕...'
    mutex.acquire()
    data_list.append(searchInfo)
    mutex.release()
    return searchInfo

'''
以下为url获取
'''
def getNewsDict(word,page,search_dict):
    resultDict={}
    if search_dict.get('baidu')=='true':
        baiduUrl=baiduNews_search.getBaiduUrl(word,page)
        resultDict['baidu']=baiduUrl
    if search_dict.get('china_so')=='true':
        chinaUrl=chinaNews_search.getChinaUrl(word,page)
        resultDict['china_so']=chinaUrl 
    if search_dict.get('s360')=='true':
        s360Url=s360News_search.gets360Url(word, page)
        resultDict['s360']=s360Url
    if search_dict.get('sogou')=='true':
        sogouUrl=sogouNews_search.getSogouUrl(word, page)
        resultDict['sogou']=sogouUrl
    return resultDict
   
def getPagesDict(word,page,search_dict):
    resultDict={}
    if search_dict.get('baidu')=='true':
        baiduUrl='https://www.baidu.com/s?wd='+word+'&pn='+str(10*(page-1))
        resultDict['baidu']=baiduUrl
    if search_dict.get('china_so')=='true':
        chinaUrl='http://www.chinaso.com/search/pagesearch.htm?q='+word+'&page='+str(page)+'&wd='+word 
        resultDict['china_so']=chinaUrl
    if search_dict.get('s360')=='true':
        s360Url='https://www.so.com/s?q='+word+'&pn='+str(page)
        resultDict['s360']=s360Url
    if search_dict.get('sogou')=='true':
        sogouUrl='http://www.sogou.com/web?query='+word+'&ie=utf8&page='+str(page)
        resultDict['sogou']=sogouUrl
    if search_dict.get('bing')=='true':
    #    cvid=getBingCVID()
        if page<=1:
            page=1
        else:
            page=(page-1)*10
        #bingUrl='https://www.bing.com/search?q='+word+'&first='+str(page)+'&cvid='+cvid+'&FORM=PERE'
        bingUrl='https://www.bing.com/search?q='+word+'&first='+str(page)+'&FORM=PERE'
        resultDict['bing']=bingUrl
    if search_dict.get('shen_ma')=='true':
        base64_text = base64.encodestring(word).strip()
        base64_text=base64_text.replace('+','!') #神马搜索会把编码后的文字中的'+'换成'!'
        shenmaUrl=None
        if(page==1):
            shenmaUrl=u'http://aibing.cc/shenma/'+base64_text+u'.html'
        else:
            shenmaUrl=u'http://aibing.cc/shenma/'+base64_text+'_'+str(page)+u'.html'
        if shenmaUrl is not None:
            resultDict['shen_ma']=shenmaUrl
    return resultDict

def getUrlDict(word,page,content_type,search_dict):
    if content_type=='1': #获取新闻url
        return getNewsDict(word,page,search_dict)
    elif content_type=='2': #获取网页url
        return getPagesDict(word,page,search_dict)
    else:
        print 'error,bad content_type argument'
    return None
'''
以下为新闻搜索
'''
#百度新闻，page从1开始
def baidu_news_search(word ,page,delay=False):
    if(delay):
        time.sleep(0.2*page)
    #print '正在搜索百度新闻...'
    resultDict=baiduNews_search.baiduNews_info(keyword=word,page=page)
    if resultDict is None:
        print "error in baidu news"
    #print '百度新闻搜索完毕...'
    mutex.acquire()
    data_list.append(resultDict)
    mutex.release()
#中国搜索新闻，page从1开始    
def china_news_search(word ,page,delay=False):
    if(delay):
        time.sleep(0.2*page)
    #print '正在搜索中国搜索新闻...'
    resultDict=chinaNews_search.chinaNews_info(keyword=word,page=page)
    if resultDict is None:
        print "error in china news"
    #print '中国搜索新闻搜索完毕...'
    mutex.acquire()
    data_list.append(resultDict)
    mutex.release()   
#360搜索新闻，page从1开始
def s360_news_search(word ,page,delay=False):
    if(delay):
        time.sleep(0.2*page)
    #print '正在搜索360新闻...'
    resultDict=s360News_search.s360News_info(keyword=word,page=page)
    if resultDict is None:
        print "error in 360 news"
    #print '360新闻搜索完毕...'
    mutex.acquire()
    data_list.append(resultDict)
    mutex.release() 
#搜狗搜索新闻，page从1开始
def sogou_news_search(word ,page,delay=False):
    if(delay):
        time.sleep(0.2*page)
    #print '正在搜索搜狗新闻...'
    resultDict=sogouNews_search.sogouNews_info(keyword=word,page=page)
    #print '搜索新闻搜索完毕...'
    if resultDict is None:
        print "error in sogou news"
    mutex.acquire()
    data_list.append(resultDict)
    mutex.release() 
    
#新闻搜索并发，搜索特定网站特定页新闻
def news_threading_page(word ,i,search_dict):
    global data_list, mutex
    mutex = threading.Lock()
    threads = []
    data_list=[]
    if(search_dict.has_key('baidu') and search_dict['baidu']=='true'):
        threads.append(threading.Thread(target=baidu_news_search, args=(word, i)))
    if(search_dict.has_key('s360') and search_dict['s360']=='true'):
        threads.append(threading.Thread(target=s360_news_search, args=(word, i)))
    if(search_dict.has_key('sogou') and search_dict['sogou']=='true'):
        threads.append(threading.Thread(target=sogou_news_search, args=(word, i)))
    if(search_dict.has_key('china_so') and search_dict['china_so']=='true'):
        threads.append(threading.Thread(target=china_news_search, args=(word, i)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return data_list    
# 使用gevent异步协程并发爬取所有搜索引擎前i页的内容
def asynchronous(word,i):
    global data_list
    data_list=[]

    threads_baidu = [gevent.spawn(baidu_search, word,i) for i in xrange(i)]
    threads_360 = [gevent.spawn(s360_search, word,i) for i in xrange(i)]
    threads_china = [gevent.spawn(china_search, word,i) for i in xrange(i)]
    threads_bing = [gevent.spawn(bing_search, word,i) for i in xrange(i)]
    threads_sogou = [gevent.spawn(sogou_search, word,i) for i in xrange(i)]
    threads_shen_ma = [gevent.spawn(shen_ma_search, word,i) for i in xrange(i)]

    all_threads = threads_baidu + threads_360 + threads_china + threads_bing + threads_sogou + threads_shen_ma
    gevent.joinall(all_threads)
    return data_list

# 使用gevent异步协程并发爬取所有搜索引擎第i页的内容
def asynchronous_page(word, i, search_dict):
    if 'threading' in sys.modules:
        del sys.modules['threading']
    monkey.patch_all()
    global data_list

    data_list=[]

    threads_baidu = [gevent.spawn(baidu_search, word,i) ]
    threads_360 = [gevent.spawn(s360_search, word,i) ]
    threads_china = [gevent.spawn(china_search, word,i) ]
    threads_bing = [gevent.spawn(bing_search, word,i)]
    threads_sogou = [gevent.spawn(sogou_search, word,i) ]
    threads_shen_ma = [gevent.spawn(shen_ma_search, word,i)]

    all_threads=threads_baidu+threads_360+threads_china+threads_bing+threads_sogou+threads_shen_ma
    gevent.joinall(all_threads)

    return data_list

# 使用Multiprocessing 线程并发爬取所有搜索引擎第i页的内容
def multi_thread_page(word ,i,search_dict):
    global data_list
    data_list=[]
    pool = ThreadPool(4)

    if(search_dict['baidu']=='true'):
        pool.apply_async(baidu_search, (word,i ))
    if(search_dict['s360']=='true'):
        pool.apply_async(s360_search, (word,i  ))
    if(search_dict['sogou']=='true'):
        pool.apply_async(sogou_search, (word,i  ))
    if(search_dict['bing']=='true'):
        pool.apply_async(bing_search, (word,i  ))
    if(search_dict['china_so']=='true'):
        pool.apply_async(china_search, (word,i  ))
    if(search_dict['shen_ma']=='true'):
        pool.apply_async(shen_ma_search, (word,i  ))

    pool.close()
    pool.join()

    return  data_list

# 使用python　thread线程库并发爬取所有搜索引擎第i页的内容
def thread_page(word ,i,search_dict):
    global data_list
    data_list=[]

    if(search_dict['baidu']=='true'):
        thread.start_new_thread(baidu_search, (word,i ))
    if(search_dict['s360']=='true'):
        thread.start_new_thread(s360_search, (word,i  ))
    if(search_dict['sogou']=='true'):
        thread.start_new_thread(sogou_search, (word,i  ))
    if(search_dict['bing']=='true'):
        thread.start_new_thread(bing_search, (word,i  ))
    if(search_dict['china_so']=='true'):
        thread.start_new_thread(china_search, (word,i  ))
    if(search_dict['shen_ma']=='true'):
        thread.start_new_thread(shen_ma_search, (word,i  ))

    return  data_list


# 使用python　threading线程库并发爬取所有搜索引擎第i页的内容
def threading_page(word ,i,search_dict):
    global data_list, mutex
    mutex = threading.Lock()
    threads = []
    data_list=[]

    if(search_dict['baidu']=='true'):
        threads.append(threading.Thread(target=baidu_search, args=(word, i)))
    if(search_dict['s360']=='true'):
        threads.append(threading.Thread(target=s360_search, args=(word, i)))
    if(search_dict['sogou']=='true'):
        threads.append(threading.Thread(target=sogou_search, args=(word, i)))
    if(search_dict['bing']=='true'):
        threads.append(threading.Thread(target=bing_search, args=(word, i)))
    if(search_dict['china_so']=='true'):
        threads.append(threading.Thread(target=china_search, args=(word, i)))
    if(search_dict['shen_ma']=='true'):
        threads.append(threading.Thread(target=shen_ma_search, args=(word, i)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return data_list

'''
def testThreading_page(word,search_dict):
    sleepTime=1
    startTime=time.clock()
    try:
        for i in xrange(1,11):
            print 'parsing page ',i
            dataList=threading_page(word, i, search_dict)
            #print dataList
            
            if i!=10:
                time.sleep(sleepTime)
            
    except Exception:
        print format_exc()
    endTime=time.clock()
    print 'spend %f seconds' % (endTime-startTime)
'''    
# 使用python　threading线程库并发爬取所有搜索引擎前pn页的内容
def threading_all_page(word ,pn,search_dict):
    global  data_list, mutex
    mutex = threading.Lock()
    threads = []
    data_list=[]

    if(search_dict['baidu']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=baidu_search, args=(word,i,True)))
    if(search_dict['s360']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=s360_search, args=(word,i,True)))
    if(search_dict['sogou']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=sogou_search, args=(word,i,True)))
    if(search_dict['bing']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=bing_search, args=(word,i,True)))
    if(search_dict['china_so']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=china_search, args=(word,i ,True)))
    if(search_dict['shen_ma']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=shen_ma_search, args=(word,i,True)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return  data_list


# 使用python multiprocessing 进程池并发爬取所有搜索引擎第页的内容
def multi_page(word ,i):
    global  data_list
    data_list=[]
    pool = Pool(6)

    pool.apply_async(baidu_search, (word,i ))
    pool.apply_async(s360_search, (word,i  ))
    pool.apply_async(sogou_search, (word,i  ))
    pool.apply_async(bing_search, (word,i  ))
    pool.apply_async(china_search, (word,i  ))
    pool.apply_async(shen_ma_search, (word,i  ))

    pool.close()
    pool.join()
    return data_list

# 对搜索引擎搜索结果进行过滤
def match_process(datalist,harmwords):
    datalist_filted=[]
    for data  in datalist:
        try:
            content = data["abstract"]
            data["count"]=0

            for  harmword in harmwords:
                word_harm = harmword['word']
                # 若有特征词在搜索结果摘要中，进行标记
                if(str(word_harm) in str(content)):
                    data["abstract"] += '----'+str(harmword['id'])+':'+word_harm
                    data["count"] += 1

            if(data["count"]!=0):
                datalist_filted.append(data)
                #print data["title"],data["count"]
        except:
            pass

    return datalist_filted


# 使用Multiprocessing 多进程过滤搜索引擎返回结果
def word_match(data_lists, harmwords):
    reload(sys)
    sys.setdefaultencoding('utf8')
    data_list=div_list(data_lists,4)

    # 设置　multiprocessing　进程池需要开启的进程数量，为充分利用CPU,进程数应该等于CPU逻辑核心的数量
    pool = multiprocessing.Pool(processes=4)
    results = []
    filted_results=[]
    for i in xrange(4):
        # 将数据切分分配给各个子进程,并将子进程处理的结果放到results 列表中
        results.append(pool.apply_async(match_process, ( data_list[i],harmwords)))
    pool.close()
    pool.join()
    print "word match done."

    # 将　results　列表中存放的　applyresult(子进程返回结果)中的数据取出，合并到　filted_results　列表中
    for  result in results:
        items=result.get()
        for item in items:
            filted_results.append(item)
    #print 'final list :',len(filted_results)
    return filted_results

# 使用Multiprocessing 多进程过滤搜索引擎返回结果（不使用进程池）
def multiproc(data_lists,harmwords):
    global  data_list_m
    data_list_m=[]
    data_list=div_list(data_lists,4)
    threads = [multiprocessing.Process(target=match_process, args=( data_list[i],harmwords)) for i in xrange(4)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return  data_list

if __name__ == "__main__":

    search_dict={'baidu':'true','s360':'true','bing':'true','sogou':'true','shen_ma':'true','china_so':'true'}
    mydata=getUrlDict("中科院",1,1,search_dict)
    mydata = json.dumps(mydata, ensure_ascii=False)
    print mydata
    
    mydata=getUrlDict("中科院",1,2,search_dict)
    mydata = json.dumps(mydata, ensure_ascii=False)
    print mydata
    '''
    mydata=s360_search ("中科院信工所",1,delay=False)
    mydata = json.dumps(mydata, ensure_ascii=False)
    print mydata
    '''
    
    '''
    search_dict={'baidu':'true','sogou':'true','s360':'true','bing':'true','china_so':'true','shen_ma':'true'}
    testThreading_page("中国", search_dict)
    '''
    '''
    #mydata=threading_page("习近平",2, search_dict)
    #mydata=news_threading_page("习近平",1, search_dict)
#     print mydata
    #mydata = json.dumps(mydata, ensure_ascii=False)
    #print mydata
    '''
    
