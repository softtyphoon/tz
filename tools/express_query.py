

import argparse
import urllib2
import urllib
import os
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

def try_code(num):
  opener = urllib2.OpenerDirector()
  if _use_proxy is True:
    # handler = urllib2.ProxyHandler({'http': '61.184.192.42:80'})
    handler = urllib2.ProxyHandler({'http': '61.54.221.200:3128'})
    opener.add_handler(handler)
    # opener = urllib2.build_opener(handler)
    # urllib2.install_opener(opener)
    # response = urllib2.urlopen(_url)
    # print response.read()
    # return 0
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  # opener = urllib2.build_opener(handler)
  req = urllib2.Request(_url)
  for (name, val) in _header.items():
    req.add_header(name, val)
  try:
    response = opener.open(req)
  except:
    # print '10060 error, sleep 10 second'
    print 'sleep'
    time.sleep(10)
    return '0'
  content = response.read()
  # print content
  bs_page =  BeautifulSoup(gzdecode(content))
  # bs_page =  BeautifulSoup(content)
  # print bs_page
  # return 0
  sxm = json.loads(bs_page.p.get_text())
  if sxm['message'] == 'ok':
    print sxm['message']
    return 1
  else:
    print sxm['message']
    return 0
  # print sxm['data']
  # print sxm['data'][0]['ftime']
  # print json.loads(bs_page.p.get_text())
  # print bs_page.contents[0]

def code_write(fp, num):
  fp.writelines(num)

def main():
  _file = open(_file_name, 'a')
  a = 0
  while True:
    b = try_code('code')
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
    d = try_code(code)
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