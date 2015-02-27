

import argparse
import urllib2
import urllib
import os
# import get_proxy_list from proxy_extractor
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

import httplib
import StringIO, gzip
import random
import time
import json

# http://www.kuaidi100.com/chaxun?com=usps&nu=LN633399366CN 218.5.74.174
# http://proxy.com.ru/list_1.html
_file_name = 'code.txt'
_use_proxy = True
# _use_proxy = False
_url = 'http://www.kuaidi100.com/query?type=usps&postid=LN633399366CN&id=1&valicode=&temp=0.9436875737737864'
# _url = 'http://www.kuaidi100.com/chaxun?com=usps&nu=LN633399366CN'
# _url = 'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1=LN633399366CN'
# _file = None
_header = {'Accept': '*/*',
           'X-Requested-With': 'XMLHttpRequest',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Referer': 'http://www.kuaidi100.com/global/usps.shtml?from=openv',
           'Accept-Encoding': 'gzip, deflate',
           'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.3197.400',
           'Host': 'www.kuaidi100.com',
           'Proxy-Connection': 'Keep-Alive'}

def gzdecode(data):
  compressedstream = StringIO.StringIO(data)
  gziper = gzip.GzipFile(fileobj=compressedstream)
  data2 = gziper.read()
  return data2

def try_code(proxy):
  opener = urllib2.OpenerDirector()
  print proxy
  if _use_proxy is True:
    handler = urllib2.ProxyHandler({'http': '218.90.174.167:3128'})
    # handler = urllib2.ProxyHandler({'http': proxy['ip']+':'+proxy['port']})
    opener.add_handler(handler)
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  req = urllib2.Request(_url)
  for (name, val) in _header.items():
    req.add_header(name, val)
  try:
    print 'a'
    response = opener.open(req, timeout=5)
  except:
    # proxy is cann't be used
    print 'b'
    return 2
  content = response.read()
  try:
    gz = gzdecode(content)
  except:
    print content
    return 2
  bs_page =  BeautifulSoup(gz)
  sxm = json.loads(bs_page.p.get_text())
  if sxm['message'] == 'ok':
    print sxm['message']
    return 1
  else:
    print sxm['message']
    return 0

def code_write(fp, num):
  fp.writelines(num)

def  get_proxy_list(url, num):
  proxy_list = list()
  opener = urllib2.OpenerDirector()
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  req = urllib2.Request(url)
  response = opener.open(req)
  content = response.read()
  bs = BeautifulSoup(content)
  # print bs
  tag_b = bs.find_all('b')
  st = False
  cnt = 0
  for a in tag_b:
    ip_indexa = a.next_sibling
    if ip_indexa is not None and ip_indexa.string == str(num*50-50+1):
      st = True
    if st == True:
      ip_index = ip_indexa.next_sibling
      ip = ip_index.next_sibling
      # print ip_index.string, ip.string
      proxy = {'ip':ip_index.string,
               'port':ip.string}
      proxy_list.append(proxy)
      cnt = cnt + 1
    if cnt == 50:
      return proxy_list

def main():
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