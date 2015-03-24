

import argparse
import urllib2
import urllib
import os
# import get_proxy_list from proxy_extractor
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

from xml_parser import xml_parser

import httplib
import StringIO, gzip
import random
import copy
import time
import json

# http://www.kuaidi100.com/chaxun?com=usps&nu=LN633399366CN 218.5.74.174
# http://proxy.com.ru/list_1.html
_file_name = 'code.txt'
# _use_proxy = True
_use_proxy = False
# _url = 'http://www.kuaidi100.com/query?type=usps&postid=LN633399366CN&id=1&valicode=&temp=0.9436875737737864'
_url = 'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=LN633399366CN'
_usps_url = 'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1='
# _file = None
_header = {'Accept': '*/*',
           'X-Requested-With': 'XMLHttpRequest',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           # 'Referer': 'http://www.kuaidi100.com/global/usps.shtml?from=openv',
           'Accept-Encoding': 'gzip, deflate',
           'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.3197.400',
           # 'Host': 'www.kuaidi100.com',
           'Proxy-Connection': 'Keep-Alive'
           }

_usps_format = ['date', 'status', 'location']

# [{'date': u'March 5, 2015,12:52 pm', 'status': u'Delivered, In/At Mailbox', 'location': u'OAK RIDGE,TN37830'}, {'date': u'March 5, 2015,8:39 am', 'status': u' Out for Delivery ', 'location': u'OAK RIDGE,TN37830'}, {'date': u'March 5, 2015,8:29 am', 'status': u' Sorting Complete ', 'location': u'OAK RIDGE,TN37830'}, {'date': u'March 5, 2015,8:16 am', 'status': u' Arrived at Unit ', 'location': u'OAK RIDGE,TN37830'}, {'date': u'February 26, 2015,10:36 am', 'status': u' Processed Through Sort Facility ', 'location': u'ISC CHICAGO IL (USPS)'}, {'date': u'', 'status': u' Origin Post is Preparing Shipment ', 'location': u''}, {'date': u'February 24, 2015,10:25 pm', 'status': u' Processed Through Sort Facility ', 'location': u'GUANGZHOU EMS,CHINA'}, {'date': u'February 24, 2015,9:18 pm', 'status': u' Acceptance ', 'location': u'CHINA'}]

class usps_query():
  def __init__(self, use_proxy=False, format=['date', 'status', 'location'], timeout = 60):
    self.header = {'Accept': '*/*',
      'X-Requested-With': 'XMLHttpRequest',
      'Accept-Language': 'zh-CN,zh;q=0.8',
      # 'Referer': 'http://www.kuaidi100.com/global/usps.shtml?from=openv',
      'Accept-Encoding': 'gzip, deflate',
      'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.3197.400',
      # 'Host': 'www.kuaidi100.com',
      'Proxy-Connection': 'Keep-Alive'
    }
    self.use_proxy = use_proxy
    self.format = format
    self.timeout = timeout
    self.name = u'usps'
    self.url = u'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1='

  def gzdecode(self, data):
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2


  def express_track(self, ln):
    url = self.url + ln
    opener = urllib2.OpenerDirector()
    if self.use_proxy is True:
      handler = urllib2.ProxyHandler({'http': proxy['ip']+':'+proxy['port']})
      opener.add_handler(handler)
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(url)
    for (name, val) in self.header.items():
      req.add_header(name, val)

    try_times = 0;
    # response = opener.open(req, timeout = self.timeout)
    while True:
      try_times = try_times + 1
      try:
        response = opener.open(req, timeout = self.timeout)
      except:
        if try_times > 5:
          return False
        else:
          opener.close()
        continue
      break

    # try:
      # response = opener.open(req, timeout = self.timeout)
    # except:
      # return self.name + u':' + u'time out'
    content = response.read()
    response.close()
    opener.close()
    try:
      gz = self.gzdecode(content)
    except:
      print content
    bs_page =  BeautifulSoup(gz)
    a = bs_page.find_all('tr', 'detail-wrapper')
    usps_info = list()
    usps_dict = dict()
    for index, usps in enumerate(a, start=0):
      usps_item = usps.find_all('p');
      for i in range(0,3):
        usps_dict[self.format[i]] = usps_item[i].get_text().strip("\r\n\t")
        usps_dict[self.format[i]] = usps_dict[self.format[i]].replace("\r\n\t", "")
        usps_dict[self.format[i]] = usps_dict[self.format[i]].replace("\t", "")
        usps_dict[self.format[i]] = usps_dict[self.format[i]].replace(u'\xa0', '')
      usps_info.append(copy.copy(usps_dict))
    return usps_info
    # print usps_info

  def info_extractor(self, exp_info):
    # print exp_info
    if exp_info[0][u'status'].lower().find(u'delivered') == -1:
      for a in exp_info:
        if a[u'location'] == u'':
          pass
        else:
          return a[u'location']
      # return exp_info[0][u'location']
    else:
      return u'delivered'

def main():
  a = usps_query()
  print a.express_track('LN633399366CN')
  # print usps_query('LN633399366CN')
  return 0
  proxy_num = 1
  info_num = 0
  faile_cnt = 0
  change_proxy = False
  while True:
    change_proxy = False
    # get proxy list
    proxy_url = 'http://proxy.com.ru/list_'+str(proxy_num)+'.html'
    proxy_list = get_proxy_list(proxy_url, proxy_num)
    print proxy_list
    for p in proxy_list:
      faile_cnt = 0
      # p = proxy_list[2]
      while True:
        a = try_code(p)
        if a == 2:      # timeout
          change_proxy = True
          break
        elif a == 0:    # checking faile
          faile_cnt = faile_cnt + 1
        else:
          info_num = info_num + 1
          print info_num

        if faile_cnt == 3:  # consecutive 3 times checking failed, change proxy
          change_proxy = True
          break
        # return 0

  proxy = {'ip': u'41.79.69.8', 'port': u'9090'}
  while True:
    b = try_code('code', proxy)
    if b == 0:
      print 'false'
      return 0
    a = a + b
    print a
    time.sleep(2)
  return 0
  while True:
    code = ''
    for i in range(1, 13):
      a = random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
      code = code + a
    print 'try ->>>>>>>>>>>>>>>>>>>>>>>'+code
    d = try_code(code, proxy)
    # d = '0'
    # print code+'-------------------->'+d
    if d == '0':
      continue
      break
    else:
      code_write(_file, code)
      break
  _file.flush()
  _file.close()


if __name__ == '__main__':
  main()