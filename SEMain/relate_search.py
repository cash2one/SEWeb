# encoding: utf-8

import requests
import json
import base64
import re
import threading

from traceback import format_exc
from lxml import etree

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getBaiduRelateDict(word):
    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection':'keep-alive',
        'Host':'www.baidu.com',
        'Cookie':'BAIDUID=F31C164C35C9456902BD2E82DED62027:FG=1; PSTM=1459240026; BIDUPSID=A374184AC82E6781BC2986BFC8CBE674; BDSFRCVID=j9LsJeC62CKYBy5RsXUyb4JDnKzhvP3TH6aoi6G_szxX7i3b8ielEG0PJ7lQpYD-hILjogKK0mOTHvbP; H_BDCLCKID_SF=tJPtoCt2JIvSDn4kKJL_-P4DenQieRJZ5mAqot0-34cxHU_GWl5j-60m0UTLq4RftgOnaIQqWR0MfpvgyUjZ3U_BX4-jBho43bRT0DOsL4JZs56N-lQphP-UyN3LWh37bDrTVDKhJDtbMC_r247Eb-_eqx5Ka43tHD7yWCvgMIb5OR5JLtQV3ptTDM6N5fnKbmcHWhO15hvvhb3O3MA-yUKWjJ7U5xoXyGceoUQF545zSlux0bOchh_QWt8LJPnCKDOMahkM5h7xOKLG05CBj6vBDHAsaPRJ5CtXQ458K4__Hn7zepQCXbtpbt-qJt7wQ5TIWfobKxbos4ovLUvJyTL0KxbnBT5Ka5IeBJjy-pbmEl5oQqnK2R8kQN3T-URQL6RkKTCyyx3kDn3oyT3VXp0n5x5Tqj_ffR4f_CLQb-3bK4jnh-nhbKCShUFsabOT-2Q-5hOy3KOCol4G0RbDylKm5PTl5jJPQ6TUa43g-pu-hpFuDjtBD5b0jGRf-b-X-C7QW-5eHJOoDDvdqfr5y4LdLp7xJhjzBnTNQh6uyDoqMtJm5lol5q-P5POjWjKeWJLq_KPKtDK5bnO1MtbOq4_jMqrt2D62aKDs2q3o-hcqEpO9QTbS0-Fp0lbuhU3rJRbEMMJ7HlcfjlbVLxt5DUThjNK8J5KJtR3fL-08-ROSDP5gq4bohjPIbJ3eBtQmJJu8Wb5X3UjCqp6z3bJFhbbWhJJU3l-qQg-q3lTkXKb-b-bD56oT3htLyxCO0x-jLgQ9WUjMyl-VOnRX3tnJyUnQhtnnBn5aLnLf_IP2fC0MbP365IT85tk8qxbXq-I8BT7Z0l8KtqOvoqowjq55WhL--GOZ0P6iMDbqbIOmWIQHDnICQpn52RkRjUue5jv05CJ4KKJxWD3SVtJXQKcsyfAqhUJiB5OLBan7LJoxfJOKHIClj58beM5; BDUSS=FvMXVKUW4tVXRxSW9-eVNubUIxLU5-T3V6RFRGd0l6cEdvVFBidTM3NGEwWEZYQVFBQUFBJCQAAAAAAAAAAAEAAAArxB0S0sDIu86qxONfRmx5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABpESlcaREpXeU; ispeed_lsm=0; BDRCVFR[IoBQEhO7fdb]=mk3SLVN4HKm; BD_CK_SAM=1; H_PS_PSSID=; BD_UPN=12314353; sugstore=0; H_PS_645EC=9d68y2N4C0CTOH7YCRGTI4vCIA1v6KAhwuku29Cb9ttvPNNCXW%2FwVAjTdANp1AsZhlFW13GX',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'     
    }
    baiduUrl='https://www.baidu.com/s?wd='+word
    baiduSuffix='https://www.baidu.com'
   # print '正在获取百度相关搜索...'
    try:
        response=requests.get(url=baiduUrl,headers=header)
    except:
        print format_exc()
        return None
    tree = etree.HTML(response.text)  
    rs=tree.xpath('/html/body/div[@id="wrapper"]/div[@id="wrapper_wrapper"]/div[@id="container"]/div[@id="rs"]')
    if rs is not None and len(rs)>0:
        allth=rs[0].xpath('./table//th')
        mutex.acquire()
        for th in allth:
            try:
                a=th.xpath('./a')[0]
                title=a.xpath('string(.)').strip()
                href=baiduSuffix+a.attrib.get('href')
                
                if(datas.has_key(title)):
                    datas[title]=datas[title]+';baidu'
                else:
                    datas[title]='baidu'
                               
            except:
                pass
        mutex.release()  
   # print '百度相关搜索获取完毕...'
  
def getChinaRelateDict(word):
    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
        'Connection':'keep-alive',
        'Host':'www.chinaso.com',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }
    url='http://www.chinaso.com/search/pagesearch.htm?q='+word
    chinaSuffix='http://www.chinaso.com'
    #print '正在获取中国搜索相关搜索...'   
    try:
        response=requests.get(url=url,headers=header)
    except:
        print format_exc()
        return None 
    tree=etree.HTML(response.text)   
    relatedSe=tree.xpath('/html/body/div[@class="btWrapper"]/dl[contains(@class,"relatedSe")]')
    if relatedSe is not None and len(relatedSe)>0:
        allSpan=relatedSe[0].xpath('.//span')
        mutex.acquire()
        for span in allSpan:
            try:
                a=span.xpath('./a')[0]
                title=a.xpath('string(.)').strip()
                href=chinaSuffix+a.attrib.get('href')
                
                if(datas.has_key(title)):
                    datas[title]=datas[title]+';china_so'
                else:
                    datas[title]='china_so'
                                  
            except:
                pass 
        mutex.release()        
    #print '中国搜索相关搜索获取完毕...'

def getShenmaRelateDict(word): 
    # 神马搜索页面URL需要进行BASE64编码转换
    base64_text = base64.encodestring(word).strip()
    base64_text=base64_text.replace('+','!') #神马搜索会把编码后的文字中的'+'换成'!'
    url=u'http://aibing.cc/shenma/'+base64_text+u'.html'
   # print '正在获取神马搜索相关搜索...'
    try:
        response=requests.get(url=url)
    except Exception:
        print format_exc()
        return None
    tree = etree.HTML(response.text)   
    xglist=tree.xpath('/html/body/div[@id="hd_main"]/div[@id="res"]/div[@class="xglist"]')
    if xglist is not None and len(xglist)>0:
        allLi=xglist[0].xpath('.//li')
        mutex.acquire()
        for li in allLi:
            try:
                a=li.xpath('./a')[0]
                title=a.xpath('string(.)').strip()
                href=a.attrib.get('href')
                
                if(datas.has_key(title)):
                    datas[title]=datas[title]+';shen_ma'
                else:
                    datas[title]='shen_ma'
                                
            except:
                pass 
        mutex.release()        
    #print '神马搜索相关搜索获取完毕...'

def gets360RelateDict(word): 
    header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Host':'www.so.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36 '   
    }
    url='https://www.so.com/s?q='+word
    s360Suffix='https://www.so.com'
    #print '正在获取360相关搜索...'
    try:
        response=requests.get(url=url,headers=header)
    except:
        print format_exc()
        return None  
    tree = etree.HTML(response.text.encode(response.encoding).decode('utf-8')) 
    mod_relation=tree.xpath('/html/body//div[@class="mod-relation"]')
    if mod_relation is not None and len(mod_relation)>0:
        rs=mod_relation[0].xpath('./div[@id="rs"]')
        if rs is not None and len(rs)>0:
            allth=rs[0].xpath('./table//th')
            mutex.acquire()
            for th in allth:
                try:
                    a=th.xpath('./a')[0]
                    title=a.xpath('string(.)').strip()
                    href=s360Suffix+a.attrib.get('href')
                    
                    if(datas.has_key(title)):
                        datas[title]=datas[title]+';s360'
                    else:
                        datas[title]='s360'
                                        
                except:
                    pass 
            mutex.release()
   # print '360相关搜索获取完毕...'   

def getSogouRelateDict(word):
    url='http://www.sogou.com/web?query='+word
    sogouSuffix='http://www.sogou.com/web'
    # 设置请求header,防止被ban,可在浏览器中提取
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
        'Connection':'keep-alive',
        'Host':'www.sogou.com',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    }
    #print  '正在获取搜狗相关搜索...'
    try:
        response=requests.get(url=url, headers=headers)
    except Exception:
        print format_exc()
        return None
    tree = etree.HTML(response.text)
    hintBox=tree.xpath('/html/body/div[@class="wrap"]/div[@class="hintBox"]')
    if hintBox is not None and len(hintBox)>0:
        alltd=hintBox[0].xpath('.//td')
        mutex.acquire()
        for td in alltd:
            try:
                a=td.xpath('./a')[0]
                title=a.xpath('string(.)').strip()
                href=sogouSuffix+a.attrib.get('href')
                
                if(datas.has_key(title)):
                    datas[title]=datas[title]+';sogou'
                else:
                    datas[title]='sogou'                
            except:
                pass
        mutex.release()   
    #print '搜狗相关搜索获取完毕...'     

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

def getBingRelateDict(word):
    header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection':'keep-alive',
            'Host':'cn.bing.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    }
    #print '正在获取bing相关搜索...'
    cvid=getBingCVID()
    if cvid is None:
        return None
    url='https://www.bing.com/search?q='+word+'&first=1&cvid='+cvid+'&FORM=PERE'
    bingSuffix='http://cn.bing.com/'
    try:
        response=requests.get(url,headers=header)
    except Exception:
        print format_exc()
        return None
    tree = etree.HTML(response.text)
    b_context=tree.xpath('/html/body/div[@id="b_content"]/ol[@id="b_context"]') 
    if b_context is not None and len(b_context)>0:
        relateLi=None
        allLi=b_context[0].xpath('.//li')
        for li in allLi:
            try:
                text=li.xpath('./h2')[0].xpath('string(.)').strip()
                if text=='相关搜索':  #找到了相关搜索的节点
                    relateLi=li
                    break;    
            except:
                pass
        if relateLi is not None:
            allLi=relateLi.xpath('.//li')
            mutex.acquire()
            for li in allLi:
                try:
                    a=li.xpath('./a')[0]
                    title=a.xpath('string(.)').strip()
                    href=bingSuffix+a.attrib.get('href')        
                    if(datas.has_key(title)):
                        datas[title]=datas[title]+';bing'
                    else:
                        datas[title]='bing'                    
                except:
                    print format_exc()
            mutex.release()
   # print 'bing相关搜索获取完毕...'     
          
def threading_page(word,search_dict):
    global datas, mutex
    mutex = threading.Lock()
    threads = []
    datas={}
    '''
    if(search_dict['baidu']=='true'):
        threads.append(threading.Thread(target=getBaiduRelateDict,kwargs={'word':word}))
    if(search_dict['s360']=='true'):
        threads.append(threading.Thread(target=gets360RelateDict,kwargs={'word':word}))
    if(search_dict['sogou']=='true'):
        threads.append(threading.Thread(target=getSogouRelateDict,kwargs={'word':word}))
    if(search_dict['bing']=='true'):
        threads.append(threading.Thread(target=getBingRelateDict,kwargs={'word':word}))
    if(search_dict['china_so']=='true'):
        threads.append(threading.Thread(target=getChinaRelateDict,kwargs={'word':word}))
    #if(search_dict['shen_ma']=='true'):
     #   threads.append(threading.Thread(target=getShenmaRelateDict,kwargs={'word':word}))
    '''
    threads.append(threading.Thread(target=getBaiduRelateDict,kwargs={'word':word}))
    threads.append(threading.Thread(target=gets360RelateDict,kwargs={'word':word}))
    threads.append(threading.Thread(target=getSogouRelateDict,kwargs={'word':word}))
    threads.append(threading.Thread(target=getBingRelateDict,kwargs={'word':word}))
    threads.append(threading.Thread(target=getChinaRelateDict,kwargs={'word':word}))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    if '' in datas.keys():
        datas.pop("",None)
    return datas  
                                       
if __name__ == "__main__":
    search_dict={'baidu':'true','s360':'true','sogou':'true','bing':'true','china_so':'true','shen_ma':'true'}
    word='习近平'
    mydata=threading_page(word,search_dict)
    mydata = json.dumps(mydata, ensure_ascii=False)
    print mydata
