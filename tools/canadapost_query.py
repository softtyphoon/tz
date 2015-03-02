
import argparse
import urllib2
import cookielib
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

_use_proxy = False
_start_header = {
  u'Accept': u'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/xaml+xml, application/x-ms-xbap, application/x-ms-application, */*',
  u'Accept-Language': u'zh-cn',
  u'User-Agent': u'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.3197.400',
  u'Accept-Encoding': u'gzip, deflate',
  u'Proxy-Connection': u'Keep-Alive',
  u'Host': u'www.canadapost.ca'
}


def gzdecode(data):
  compressedstream = StringIO.StringIO(data)
  gziper = gzip.GzipFile(fileobj=compressedstream)
  data2 = gziper.read()
  return data2

def get_cookie(url, header, cookie_dict):
  cookie = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
  # opener = urllib2.OpenerDirector()
  if _use_proxy is True:
    handler = urllib2.ProxyHandler({'http': proxy['ip']+':'+proxy['port']})
    opener.add_handler(handler)
  http_handler = urllib2.HTTPHandler()
  https_handler = urllib2.HTTPSHandler()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)
  req = urllib2.Request(url)
  for (name, val) in header.items():
    req.add_header(name, val)

  if cookie_dict is not None:
    for (name, val) in cookie_dict.items():
      opener.addheaders.append(u'Cookie', name+u'='+val)

  try:
    response = opener.open(req, timeout=5)
  except:
    print u"flase"
    return 2

  for item in cookie:
    print 'Name = '+item.name
    print 'Value = '+item.value
  return 0
  try:
    gz = gzdecode(content)
  except:
    print content



def main():
  get_cookie(u'http://www.canadapost.ca/cpo/mc/languageswitcher.jsf', _start_header, None)

if __name__ == '__main__':
  main()