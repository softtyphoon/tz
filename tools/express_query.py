

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

from canadapost_query import canadapost_query
from usps_query import usps_query
from aus_query import aus_query

_code_file = u'track_number.txt'

def main():
  cq = canadapost_query()
  uq = usps_query()
  aq = aus_query()
  fn = open(_code_file)
  count = 1;
  for code in fn.readlines():
    code = code[0:13]
    if code[0:2].lower() == u'ln':
      info = uq.express_track(code)
      info_final = uq.info_extractor(info)
      print count, code, info_final
      count += 1
    if code[0:2].lower() == u'lx':
      continue
      info = aq.express_track(code)
      print code + u':' + info
      count += 1
    if code[0:2].lower() == u'lm':
      info = cq.express_track(code)
      info_final = cq.info_extractor(info)
      print count, code, info_final
      count += 1
    # if count == 100:
      # break
    # time.sleep(3)

  fn.close()
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