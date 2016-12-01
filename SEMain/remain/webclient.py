# encoding: UTF-8
from suds.client import Client  
import sys
import os

ip="192.168.239.134"
port=8080
ticket="PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiID8+PHRpY2tldD48Y29udGVudD48cHJvcGVydHkgIG5hbWU9IlRJQ0tFVF9JTkZPX1VJRCIgIHZhbHVlPSJ0ZXN0IiAgLz48cHJvcGVydHkgIG5hbWU9IlRJQ0tFVF9JTkZPX0NSRUFURVRJTUUiICB2YWx1ZT0iMjAxNi0wOS0wMiIgIC8+PHByb3BlcnR5ICBuYW1lPSJUSUNLRVRfSU5GT19TRVNTSU9OSUQiICB2YWx1ZT0iTVRRM01qZ3hNRGsyTnpjNU5BPT0iICAvPjxwcm9wZXJ0eSAgbmFtZT0iVElDS0VUX0lORk9fQ0xJRU5USVAiICB2YWx1ZT0iMTkyLjE2OC4xMjIuMSIgIC8+PHByb3BlcnR5ICBuYW1lPSJUSUNLRVRfSU5GT19VU0VSSUQiICB2YWx1ZT0iOTY4IiAgLz48cHJvcGVydHkgIG5hbWU9IlRJQ0tFVF9JTkZPX0RFRklORV9VU0VSUFJPVklOQ0VJRCIgIHZhbHVlPSIwMCIgIC8+PHByb3BlcnR5ICBuYW1lPSJUSUNLRVRfSU5GT19ERUZJTkVfVVNFUlNOIiAgdmFsdWU9IjAwMDMxMDAwODEiICAvPjwvY29udGVudD48c2lnbmF0dXJlcz48c2lnbmF0dXJlIGFsZz0iMS4yLjg0MC4xMTM1NDkuMS4xLjUiIGVuY29kaW5nPSJiYXNlNjQiIHNpZ25ieT0iMTcwNTAwMDAwMDAwMDAzZSIgPm5CVHkrM2poaGVhTVRkdjVyZmtmc09EVCsyNzBnNWVNdzhybktyQS9qUTNRL1BCNDJnTlNqWHdERTMzcGU3Zm8zdmVrSDU4djJTL2YrK3RrZHpQQmVMUjJHVTFzdzdMdHhNNjVDSXlSOW9xSXlJUmF2RjBGdzcwcjZJUFJCejZMUTlwS29PUk5WWExTN3FCdWhEMTdyZ3ZObE8zTmxnRk0vZ2dnVkhpVUJNbz08L3NpZ25hdHVyZT48L3NpZ25hdHVyZXM+PC90aWNrZXQ+"

#def class MyTicket(object):



def login():
    client = Client("http://%s:%s/WebServices/services/AuthServer?wsdl" % (ip, port),)
    print client
    client.options.cache.clear()
    result= client.service.parseTicket(ticket)
    print result
    print result.sessionID
    result=client.service.verifyTicket(ticket)
    print result
if __name__ == '__main__':
    login()
    client = Client("http://192.168.239.134:8080/WebServices/services/AuthRight?wsdl",)
    print client
   # client = Client("http://192.168.239.134:8080/WebServices/services/AuditManager?wsdl",)
   # print client



