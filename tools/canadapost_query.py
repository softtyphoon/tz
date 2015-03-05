
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

_query_header = {
  u'Accept-Language': u'zh-CN,zh;q=0.8',
  u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  u'Referer': u'http://www.canadapost.ca/cpo/mc/default.jsf',
  u'Host': u'www.canadapost.ca',
  u'User-Agent': u'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.3345.400',
  u'Accept-Encoding': u'gzip, deflate',
  u'Proxy-Connection': u'Keep-Alive',
  u'Cookie': u'LANG=e; style=0; languageset=t; ct=true; homeReferrer='
}

_start_header = {
  u'Origin': u'http://www.canadapost.ca',
  u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  u'Content-Type': u'application/x-www-form-urlencoded',
  u'Accept-Language': u'zh-CN,zh;q=0.8',
  u'Referer': u'http://www.canadapost.ca/cpo/mc/default.jsf?LOCALE=en',
  u'Host': u'www.canadapost.ca',
  u'User-Agent': u'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.3197.400',
  u'Accept-Encoding': u'gzip, deflate',
  u'Content-Length': u'38',
  u'Proxy-Connection': u'Keep-Alive',
  u'Pragma': u'no-cache',
  u'Cookie': u'LANG=e; style=0; languageset=t; ct=true; homeReferrer='
}
# languageset=t; LANG=e; ct=true; homeReferrer=

# trackingNumber=LM922612242CN&x=35&y=12

def gzdecode(data):
  compressedstream = StringIO.StringIO(data)
  gziper = gzip.GzipFile(fileobj=compressedstream)
  data2 = gziper.read()
  return data2

def get_cookie(url, header, cookie_dict):
  info = dict()
  cookie = cookielib.CookieJar()
  # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
  opener = urllib2.OpenerDirector()
  if _use_proxy is True:
    handler = urllib2.ProxyHandler({'http': proxy['ip']+':'+proxy['port']})
    opener.add_handler(handler)
  http_handler = urllib2.HTTPHandler()
  https_handler = urllib2.HTTPSHandler()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)
  req = urllib2.Request(url)
  # req.add_data(u'trackingNumber=LM922612242CN&x=35&y=12')
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

  print response.info().getheader('Set-Cookie')
  set_cookie = response.info().getheader('Set-Cookie')
  # search_pat = re.compile(r'CPO_SSID_PRD10_UI_CPO\s*=\s*(\d+)')
  search_pat = re.compile(r'CPO_SSID_PRD10_UI_CPO=(.+?);')
  info[u'CPO_SSID_PRD10_UI_CPO'] = search_pat.search(set_cookie).group(1)
  search_pat = re.compile(r'CPO_JSESSIONID=(.+?);')
  info[u'CPO_JSESSIONID'] = search_pat.search(set_cookie).group(1)
  content = response.read()
  for item in cookie:
    print 'Name = '+item.name
    print 'Value = '+item.value
  # return 0
  body =  BeautifulSoup(content)
  info[u'addr'] = body.find_all('a')[0].get_text()
  print repr(info)
  return info


class canadapost_query():
  def __init__(self, use_proxy):
    self.use_proxy = use_proxy
    # self.header = header
  def get_express(self, content):
    bs = BeautifulSoup(content)
    info = bs.find_all(attrs={u"class":"even"})
    print info

  # get 304 and cookie
  def get_session(self, url, header):
    info = dict()
    cookie = cookielib.CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener = urllib2.OpenerDirector()
    if _use_proxy is True:
      handler = urllib2.ProxyHandler({'http': proxy['ip']+':'+proxy['port']})
      opener.add_handler(handler)
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(url)
    req.add_data(u'trackingNumber=LM922612242CN&x=35&y=12')
    for (name, val) in header.items():
      if name is not u'Cookie':
        req.add_header(name, val)

    try:
      response = opener.open(req, timeout=5)
    except:
      print u"flase"
      return 2

    print response.info().getheader('Set-Cookie')
    set_cookie = response.info().getheader('Set-Cookie')
    search_pat = re.compile(r'CPO_SSID_PRD10_UI_CPO=(.+?);')
    info[u'CPO_SSID_PRD10_UI_CPO'] = search_pat.search(set_cookie).group(1)
    search_pat = re.compile(r'CPO_JSESSIONID=(.+?);')
    info[u'CPO_JSESSIONID'] = search_pat.search(set_cookie).group(1)
    content = response.read()
    body =  BeautifulSoup(content)
    print body
    info[u'addr'] = body.find_all('a')[0].get_text()
    return info

  def query(self, url, header, cookie_dict, sn):
    opener = urllib2.OpenerDirector()
    if self.use_proxy is True:
      handler = urllib2.ProxyHandler({'http': proxy['ip']+':'+proxy['port']})
      opener.add_handler(handler)
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(url)
    # req.add_data(u'trackingNumber='+sn+u'&x=35&y=12')
    # req.add_data(u'trackingNumber=LM922612242CN&x=35&y=12')
    for (name, val) in header.items():
      if name is not u'Content-Length' or name is not u'Origin':
        req.add_header(name, val)

    cookie = req.get_header(u'Cookie')

    if cookie_dict is not None:
      for (name, val) in cookie_dict.items():
        cookie = cookie + ';' + name + u'=' + val
        # opener.addheaders.append(u'Cookie', name+u'='+val)
    req.add_header(u'Cookie', cookie)
    try:
      response = opener.open(req, timeout=5)
    except:
      print u"flase"
      return 2

    # print response.info().getheader('Set-Cookie')
    content = response.read()

    # return 0
    try:
      gz = gzdecode(content)
    except:
      print content
      print 'gz false'
      return 0

    return gz
  # ---
  def query_a(self, url, header, cookie_dict, sn):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    if self.use_proxy is True:
      handler = urllib2.ProxyHandler({'http': proxy['ip']+':'+proxy['port']})
      opener.add_handler(handler)
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(url)
    req.add_data(u'trackingNumber='+sn+u'&x=35&y=12')
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

    print response.info().getheader('Set-Cookie')
    content = response.read()
    for item in cookie:
      print 'Name = '+item.name
      print 'Value = '+item.value
    # return 0
    try:
      gz = gzdecode(content)
    except:
      print content
      print 'gz false'
      return 0
    print gz
    return 0

def main():
  a = canadapost_query(_use_proxy)
  info = a.get_session(u'http://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber', _start_header)
  print repr(info)
  cookie_dict = dict()
  cookie_dict[u'CPO_SSID_PRD10_UI_CPO'] = info[u'CPO_SSID_PRD10_UI_CPO']
  cookie_dict[u'CPO_JSESSIONID'] = info[u'CPO_JSESSIONID']
  content = a.query(info[u'addr'], _query_header, cookie_dict, u'LM922612242CN')
  a.get_express(content)
  # a.query_a(u'http://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber', _start_header, None, u'LM922612242CN')
  # get_cookie(u'http://www.canadapost.ca/cpo/mc/languageswitcher.jsf', _start_header, None)
  # get_cookie(u'http://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber?execution=e2s1', _start_header, None)
  # get_cookie(u'http://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber', _start_header, None)       # get JSSESION and JSID and query url when not using cookie
  # get_cookie(u'http://www.canadapost.ca/cpo/mc/default.jsf?LOCALE=en', _start_header, None)

if __name__ == '__main__':
  main()