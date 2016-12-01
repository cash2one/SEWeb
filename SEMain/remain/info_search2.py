# encoding: utf-8

import base64
import multiprocessing

import thread
import threading
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import gevent
import requests
from bs4 import BeautifulSoup
from gevent import monkey

import sys
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


# 百度搜索引擎爬虫
def badiu_search(word ,page,delay=False):
    global mutex
    # 多线程请求时设置延时，防止网络拥塞及IP被BAN
    if(delay):
        time.sleep(0.1*page)
    url='http://www.baidu.com/s?wd='+word+'&pn='+str(10*(page-1))

    try:
        # 设置请求超时
        response=requests.get(url,timeout=3)
    except:
        print "connection  error --baidu"
        return

    html=response.text
    soup = BeautifulSoup(html,"lxml")

    # DOM  选择器选择页面元素
    links = soup.select('h3 a')
    abstract = soup.select('div div[class="c-abstract"]')

    for link ,abs in zip(links,abstract):
        title = link.text
        url = link.get('href')
        content =abs.text
        parameter = {
            'keyword':word,
            'topics_id':'0',
            'url':url.encode("utf-8"),
            'title':title,
            'abstract':content,
            'url_source':'baidu'
        }
        # 将页面数据保存到data_list中,线程加锁
        mutex.acquire()
        data_list.append(parameter)
        mutex.release()

        # try:
        #     db.execute(text('insert into search_infos (keyword,topics_id,url,title,abstract,url_source,update_time) \
        #  values  (:keyword,:topics_id,:url,:title,:abstract,:url_source,now())'),parameter)
        #     db.commit()
        #
        # except:
        #     print ''

    # end = time.time()
    # sys.stdout.write ('baidu')

def  s360_search (word ,page,delay=False):
    global mutex
    if(delay):
        time.sleep(0.1*page)
    # 设置请求header,防止被ban,可在浏览器中提取
    header = {
		'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Cookie':'QiHooGUID=72FE5A9CFCFB1E513B835CF6A9206470.1462255746714; tso_Anoyid=11146225574615922659; __guid=15484592.628176981503019100.1462255747200.4785; dpr=1; webp=1; erules=p2-40%7Cp1-57%7Cecl-14%7Ckd-10%7Cp3-11%7Cp4-13; _S=esg8tmq9vs1iopiaun5nm5cu84; __huid=10S%2Fenx%2Fi5EObZkV5w6UGIVboMm%2B8EiCLMWxQmk4h1uds%3D; count=4',
		'Host':'www.so.com',
		'Referer':'https://www.so.com/s?q=%E4%B9%A0%E8%BF%91&src=srp&fr=hao_search&psid=ca6a561f5acb25b7adbb547795e358ac',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
		'X-Requested-With':'XMLHttpRequest',
    }
    url='https://www.so.com/s?q='+word+'&pn='+str(page)

    print  url
    try:
        response = requests.get(url,timeout=2)
    except:
        print "connection  error --360"
        return

    #非utf-8编码的网页进行编码转换
    html = response.text.encode('ISO-8859-1').decode('utf-8')
    soup = BeautifulSoup(html,"lxml")
    links = soup.select('h3 a')

    if(page == 1):
        abstract = soup.select('li[class="res-list"] div div')
    else:
        abstract = soup.select('li  p[class="res-desc"]')

    for link ,abs in zip(links,abstract):
        title = link.text
        url = link.get('href')
        content =abs.text
        parameter={
            'keyword':word,
            'topics_id':'0',
            'url':url.encode("utf-8"),
            'title':title,
            'abstract':content,
             'url_source':'360'
        }
        mutex.acquire()
        data_list.append(parameter)
        mutex.release()

def sogou_search (word ,page,delay=False):
    global mutex
    if(delay):
        time.sleep(0.2*page)

    url='http://www.sogou.com/web?query='+word+'&page='+str(page)

    # 设置请求header,防止被ban,可在浏览器中提取
    headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Cookie':'SUV=1460162941883781; SMYUV=1460162941884122; CXID=17728DC8D9211870D64CA7C46E54E8CB; SUID=445FE29F546C860A570854F8000A8C38; ssuid=6671667376; ABTEST=6|1460945183|v17; pgv_pvi=5393779712; SNUID=AAB10F72EDEBDC070062A005EE2FC5AF; ad=ekllllllll2gjVFclllllVtIXUwlllllXMJKSllllxylllllxVxlw@@@@@@@@@@@; IPLOC=CN1100; JSESSIONID=abc1hBMqJpWphhWAUB7rv; taspeed=taspeedexist; pgv_si=s9957614592; sst0=384; ld=wkllllllll2g3QGSlllllVtILTUlllllXMJKSllllltlllllxllll5@@@@@@@@@@; browerV=3; osV=3; LSTMV=189%2C240; LCLKINT=3093; sct=31',
		'Host':'www.sogou.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    }

    print  url
    try:
        response=requests.get(url, headers=headers, timeout=5)
    except:
        print "connection  error --sogou"
        return

    html = response.text
    soup = BeautifulSoup(html,"lxml")
    links = soup.select('div[class="rb"]  h3 a')
    abstract = soup.select('div[class="rb"]  div[class="ft"]')

    for link ,abs in zip(links,abstract):
        title = link.text
        url = link.get('href')
        content =abs.text
        parameter={
            'keyword':word,
            'topics_id':'0',
            'url':url.encode("utf-8"),
            'title':title,
            'abstract':content,
            'url_source':'sogou'
        }
        mutex.acquire()
        data_list.append(parameter)
        mutex.release()
		
    links1 = soup.select('div[class="vrwrap"]  h3 a')
    abstract1 = soup.select('div[class="vrwrap"]  div div p ')


    for link ,abs in zip(links1,abstract1):
        title = link.text
        url = link.get('href')
        content =abs.text
        parameter={
            'keyword':word,
            'topics_id':'0',
            'url':url.encode("utf-8"),
            'title':title,
            'abstract':content,
            'url_source':'sogou'
        }

        mutex.acquire()
        data_list.append(parameter)
        mutex.release()

        # end = time.time()
        # sys.stdout.write ('sogou')

def china_search(word ,page,delay=False):
    global  mutex

    if(delay):
        time.sleep(0.2*page)

    # time.sleep(0.5*page)
    # start = time.time()

    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
        'Connection':'keep-alive',
        'Cookie':'uid=CgqAiVcoQK6uPDtwBJRPAg==; wdcid=1fb597e8477d563b; cookie_name=159.226.95.68.1462255802583833; wdlast=1462276278',
        'Host':'www.chinaso.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    url='http://www.chinaso.com/search/pagesearch.htm?q='+word+'&page='+str(page+1)+'&wd='+word
    print  url
    try:
        response=requests.get(url,headers=header,timeout=6)
    except:
        print "connection  error --china_search"
        return

    html=response.text
    soup = BeautifulSoup(html,"lxml")
    items = soup.select('ol[class="seResult"] li[class"]')

    for item  in  items:
        try:
           link=item.select('a')[0]
        except:
            pass
        abs=item.select('p')

        if(not abs):
            try:
                abs=item.select('div  div p')[0]
            except:
                continue
        else:
            abs=abs[0]

        title = link.text
        url = link.get('href')

        url='http://www.chinaso.com'+url

        # try:
        #     url=requests.get(url,timeout=5).url
        #
        # except:
        #     url="url can not  open "

        if(abs):
            content =abs.text
            content=content.replace(" ","").replace("\t","").strip()
        else:
            content=''

        parameter={
            'keyword':word,
            'topics_id':'0',
            'url':url.encode("utf-8"),
            'title':title,
            'abstract':content,
            'url_source':'china_so'
        }
        mutex.acquire()
        data_list.append(parameter)
        mutex.release()

        # end = time.time()
        # sys.stdout.write ('china_so')

def bing_search(word ,page,delay=False):
    global mutex
    if(delay):
        time.sleep(0.1*page)

    # start = time.time()

    url='https://www.bing.com/search?q='+word+'&first='+str(10*page)
    print  url
    try:
        response=requests.get(url,timeout=2)
    except:
        print "connection  error  --bing_search"
        return


    html=response.text
    soup = BeautifulSoup(html,"lxml")
    items = soup.select('ol[id="b_results"] li[class="b_algo"]')
    print len(items)

    for item in items:
        link=item.select('h2 a')[0]
        abs=item.select('div[class="b_caption"] p')
        if(not abs):
            abs=item.select('div div div p')[0]
            if(not abs):
                print item
        else:
            abs=abs[0]

        title = link.text
        url = link.get('href')
        content =abs.text

        # print str(page),content
        parameter={
            'keyword':word,
            'topics_id':'0',
            'url':url.encode("utf-8"),
            'title':title,
            'abstract':content,
            'url_source':'bing'
        }
        mutex.acquire()
        data_list.append(parameter)
        mutex.release()
        # end = time.time()
        # print 'bing',end-start

def shen_ma_search(word ,page,delay=False):
    global mutex
    if(delay):
        time.sleep(0.2*page)
    # start = time.time()
    # 神马搜索页面URL需要进行BASE64编码转换
    base64_text = base64.encodestring(word).strip()

    if(page==0):
        url=u'http://aibing.cc/shenma/'+base64_text+u'.html'
    else:
        url=u'http://aibing.cc/shenma/'+base64_text+'_'+str(page+1)+u'.html'

    print url
    try:
        response=requests.get(url,timeout=3)
    except:
        print "connection  error --shen_ma"
        return


    html = response.text
    soup = BeautifulSoup(html,"lxml")
    items = soup.select('div[id="result"] div[class="g"]')
    print len(items)
    for item in items:
        link=item.select('h2 a')[0]
        abs=item.select('div[class="std"]')[0]
        title = link.text
        url = link.get('href')
        url='http://aibing.cc'+url
        # 获取页面链接真实URL ,开销较高
        # try:
        #     resp=requests.get(url,timeout=5)
        #     html=resp.text
        #     url=re.findall('blank">(.*?)</a>',html)[0]
        #
        #
        # except:
        #     url="url can not  open "
        content =abs.text
        parameter={
            'keyword':word,
            'topics_id':'0',
            'url':url.encode("utf-8"),
            'title':title,
            'abstract':content,
            'url_source':'shenma'
        }
        mutex.acquire()
        data_list.append(parameter)
        mutex.release()
        # end = time.time()
        # sys.stdout.write ('shen_ma')




# 使用gevent异步协程并发爬取所有搜索引擎前i页的内容
def asynchronous(word,i):
    global data_list
    data_list=[]

    threads_baidu = [gevent.spawn(badiu_search, word,i) for i in xrange(i)]
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

    threads_baidu = [gevent.spawn(badiu_search, word,i) ]
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
        pool.apply_async(badiu_search, (word,i ))
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
        thread.start_new_thread(badiu_search, (word,i ))
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
        threads.append(threading.Thread(target=badiu_search, args=(word, i)))
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

# 使用python　threading线程库并发爬取所有搜索引擎前pn页的内容
def threading_all_page(word ,pn,search_dict):
    global  data_list, mutex
    mutex = threading.Lock()
    threads = []
    data_list=[]

    if(search_dict['baidu']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=badiu_search, args=(word,i,True)))
    if(search_dict['s360']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=s360_search, args=(word,i,True  )))
    if(search_dict['sogou']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=sogou_search, args=(word,i,True  )))
    if(search_dict['bing']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=bing_search, args=(word,i,True  )))
    if(search_dict['china_so']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=china_search, args=(word,i ,True )))
    if(search_dict['shen_ma']=='true'):
        for i in xrange(pn):
            threads.append(threading.Thread(target=shen_ma_search, args=(word,i,True  )))

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

    pool.apply_async(badiu_search, (word,i ))
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
                print data["title"],data["count"]
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
    print 'final list :',len(filted_results)
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

