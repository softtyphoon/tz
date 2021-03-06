
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
    response = opener.open(req, timeout = self.timeout)
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

# LX905296899CN
# :
# [{u'date': u'2014/12/23AM', u'location': u'ATIKAMEG', u'description': u'Item successfully delivered'}, {u'date': u'2014/12/2109:17', u'location': u'EDMONTON', u'description': u'In transit '}, {u'date': u'06:27', u'location': u'EDMONTON', u'description': u'Item processed'}, {u'date': u'2014/12/2001:38', u'location': u'RICHMOND', u'description': u'Item processed'}, {u'date': u'2014/12/1922:16', u'location': u'RICHMOND', u'description': u'Item processed at postal facility'}, {u'date': u'22:16', u'location': u'RICHMOND', u'description': u'Item was released by Customs and is now with Canada Post for processing'}, {u'date': u'20:04', u'location': u'RICHMOND', u'description': u'Item has arrived in Canada and was sent for further processing.'}, {u'date': u'01:17', u'location': u'CNCAND,China', u'description': u'International item has left originating country and is en route to Canada'}, {u'date': u'2014/12/1819:41', u'location': u'510321,China', u'description': u'International item mailed in originating country'}]

class canadapost_query():
  def __init__(self, use_proxy=False, timeout = 60):
    self.use_proxy = use_proxy
    self.timeout = timeout
    self.name = u'canadapost'
    # self.start_header = start_header
    self.start_header = {
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
    # self.query_header = query_header
    self.query_header = {
      u'Accept-Language': u'zh-CN,zh;q=0.8',
      u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      u'Referer': u'http://www.canadapost.ca/cpo/mc/default.jsf',
      u'Host': u'www.canadapost.ca',
      u'User-Agent': u'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.3345.400',
      u'Accept-Encoding': u'gzip, deflate',
      u'Proxy-Connection': u'Keep-Alive',
      u'Cookie': u'LANG=e; style=0; languageset=t; ct=true; homeReferrer='
    }
    # self.header = header
  def get_express(self, content):
    info_temp = dict()
    exp_info = list()
    bs = BeautifulSoup(content)
    info_even = bs.find_all(attrs={u"class":"even"})
    info_odd = bs.find_all(attrs={u"class":"odd"})
    info = list(range(1, len(info_even) + len(info_odd) + 1))
    info[0::2] = info_odd
    info[1::2] = info_even
    for a in info:
      str = u''
      if a.contents[0].string is not None:
        str = a.contents[0].string
      if a.contents[1].string is not None:
        str = str + a.contents[1].string
      info_temp[u'date'] = str
      info_temp[u'location'] = a.contents[2].contents[0]
      # info_temp[u'description'] = a.contents[3].contents[0].replace(u'\r\n\t', '')
      info_temp[u'description'] = a.contents[3].contents[0].strip(u'\n\t')
      exp_info.append(copy.copy(info_temp))
    # print repr(exp_info)
    return exp_info

  def info_extractor(self, exp_info):
    if exp_info[0][u'description'].lower().find(u'delivered') == -1:
       for a in exp_info:
        if a[u'location'] == u'':
          pass
        else:
          return a[u'location']
      # return exp_info[0][u'location']
    else:
      return u'delivered'

  def gzdecode(self, data):
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2

  # get 304 and cookie
  def get_session(self, url, header, ln):
    info = dict()
    cookie = cookielib.CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener = urllib2.OpenerDirector()
    if self.use_proxy is True:
      handler = urllib2.ProxyHandler({'http': proxy['ip']+':'+proxy['port']})
      opener.add_handler(handler)
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(url)
    req.add_data(u'trackingNumber='+ln+u'&x=35&y=12')
    for (name, val) in header.items():
      if name is not u'Cookie':
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

    # print response.info().getheader('Set-Cookie')
    set_cookie = response.info().getheader('Set-Cookie')
    search_pat = re.compile(r'CPO_SSID_PRD10_UI_CPO=(.+?);')
    info[u'CPO_SSID_PRD10_UI_CPO'] = search_pat.search(set_cookie).group(1)
    search_pat = re.compile(r'CPO_JSESSIONID=(.+?);')
    info[u'CPO_JSESSIONID'] = search_pat.search(set_cookie).group(1)
    content = response.read()
    response.close()
    opener.close()
    body =  BeautifulSoup(content)
    # print body
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
      # print self.name + u":" + u"flase"
      # return 2
      
    content = response.read()
    # print response.info().getheader('Set-Cookie')

    response.close()
    opener.close()
    # return 0
    try:
      gz = self.gzdecode(content)
    except:
      print content
      print 'gz false'
      return 0

    # print gz
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
      response = opener.open(req, timeout = self.timeout)
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
      gz = self.gzdecode(content)
    except:
      print content
      print 'gz false'
      return 0
    print gz
    return 0

  def express_track(self, track_num):
    info = self.get_session(u'http://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber', self.start_header, track_num)
    cookie_dict = dict()
    cookie_dict[u'CPO_SSID_PRD10_UI_CPO'] = info[u'CPO_SSID_PRD10_UI_CPO']
    cookie_dict[u'CPO_JSESSIONID'] = info[u'CPO_JSESSIONID']
    content = self.query(info[u'addr'], self.query_header, cookie_dict, track_num)
    return self.get_express(content)

def main():
  a = canadapost_query()
  print a.express_track(u'LM922612242CN')
  # a.query_a(u'http://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber', _start_header, None, u'LM922612242CN')
  # get_cookie(u'http://www.canadapost.ca/cpo/mc/languageswitcher.jsf', _start_header, None)
  # get_cookie(u'http://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber?execution=e2s1', _start_header, None)
  # get_cookie(u'http://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber', _start_header, None)       # get JSSESION and JSID and query url when not using cookie
  # get_cookie(u'http://www.canadapost.ca/cpo/mc/default.jsf?LOCALE=en', _start_header, None)

if __name__ == '__main__':
  main()