# encoding: utf-8
import time
import os.path
import datetime
import torndb
import MySQLdb
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

ISOTIMEFORMAT = '%Y-%m-%d %X'
#log_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],"logs")
#log_file = ""

def get_create_period():
	period = 24 * 60 * 60 * 1000
	return period

def get_table_name():
	table_name = 'log'+ re.sub('\-','_',str(datetime.date.today()))
	return table_name

def onServerStartCreateLogTable():
	table_name = get_table_name()
	try:
		conn = torndb.Connection("127.0.0.1:3306","jhss_log",user="root",password="!QAZ2wsx")
		exe = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' LIKE log_demo'
		conn.execute(exe)
		print 'create log table ' + table_name  
	except:
		print 'failed'
	finally:
		conn.close()

def onQueryRecordLog(ip,content_type,key,suggestion_map,relate_search_map,hint_top_map):
	key =  MySQLdb.escape_string(key)
	suggestion_map = MySQLdb.escape_string(suggestion_map)
	relate_search_map = MySQLdb.escape_string(relate_search_map)
	hint_top_map = MySQLdb.escape_string(hint_top_map)
	table_name = get_table_name()
	str_content_type = {'1':"新闻",'2':"网页",'3':"图片",'4':"右侧推荐",'5':"其他",'6':"联想词",'7':"相关搜索",'8':"为您推荐"}
	keyword = key.encode('utf-8')
	type = str_content_type[content_type].decode('gbk','ignore').encode('utf-8')#.decode('gbk','ignore')
	try:
		conn = torndb.Connection("127.0.0.1:3306","jhss_log",user="root",password="!QAZ2wsx")
		cur_time = str(time.strftime(ISOTIMEFORMAT,time.localtime()))
		suggestion_map=suggestion_map.replace(r"%",'%%')
		relate_search_map=relate_search_map.replace(r"%",'%%')
		hint_top_map=hint_top_map.replace(r"%",'%%')
		exe="INSERT INTO %s (time,ip,type,keyword,suggestion,relate_search,hint_top) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(table_name,cur_time,ip,type,keyword,suggestion_map,relate_search_map,hint_top_map)
		conn.execute(exe)
	except:
		print("errors:  %s"%(exe))
	finally:
		conn.close()

if __name__=="__main__":
	onServerStartCreateLogTable()
	onQueryRecordLog("1.1.1.1",'3',"脧掳艙眉脝艙")
