#coding:utf-8

import argparse
import urllib2
import urllib
import os
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


_host = 'http://www.chngc.net'
_jb_url = 'http://www.chngc.net/sitefiles/services/wcm/dynamic/output.aspx?publishmentSystemID=1269&Year='
_start = 1979
_end = 2010
_refer = 'http://www.chngc.net/catalog/catalogYear.html?Year='
_header = {'Origin': 'http://www.chngc.net',
           'X-Requested-With': 'XMLHttpRequest',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Proxy-Connection': 'Keep-Alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.1374.400',
           'Host': 'www.chngc.net',
           'Content-Length': '1717',
           'Pragma': 'no-cache',
           'Cookie': 'pgv_si=s9023835136'}
_data = 'pageNodeID=1319&pageContentID=0&pageTemplateID=1180&isPageRefresh=False&pageUrl=db0slash0m5tOIspnIjlM2yAwSZNvU6P1eKfuzgbuRyoeLr41BWQVWPLvvj6WhW9HCtCm9&ajaxDivID=ajaxElement_3_384&templateContent=7tU3sA46A6a8zJwJoqSjnuW6RjIO3JGmaNerM9Zetom3dR824LXNlr4UT4ZhooBwaSw0slash0pRNae0slash0g7h0slash0DQXEUDqN7gC9eBFjQvDWeRGSsedC9M1Tl1uEDV4W0uz0BWpV0add0ntPgMUDAeP30uZIA1sycP5buN542oPbllxbwRchqVMDJB0slash0AtP6Zh1NoXtNnIgOwvrwUWqK2FhyY75eLANU0add0zwXBf0add0HAxgXdRgA7b0add0N0WS4ujNmxsrPMYqewycLPZDY0YgK0kGY6C5x7gQqJn6uKD2HsuCM1vgkaJGtjgxxrH0slash0Je3TtGwifIu76Hqr0slash0sMLnJxjQ9O3CW8Ds0add0ZCtaBfUg2S4CCWPj6ko4SLzTq5ZGffcvjreA6KwevmYodJ9Qgyx6vekoD4r0add0M1eH2iH2zLm4UzOKHMWslJHLXdEM6vYeYQ5j6IGXZe4dkY19EMH1NQuCRGHevhNPvrP0add0EBgYlItSx89AXkBx408GpCR0slash0LWq0zTVrZEjECBKK9ZtQcKF8hgR0add03fkQ0zna0slash0we5Q4suacMHZjMFE85Bd1lmsUF4Re5Ota6OrXOmi0add08zzYptVRN8O9gFvnEft6JG22jwFKGGV44kdZr0add0FrJaTrkqfu0add0Pa4Hm9kgML2U79BkgY59mKbt6Naxn8kI0slash0fp7LmQz7rM5siCu5ITu3KBoIJocCqXEleeyWzvP1X5MTYMNidrLG0v8E9ng29ZoDD5wv8QNKT6lNk1xXiH20add02oDq2GCA5SffUeRqZo7HXNUVJg0oDq0slash0IUxUikgxMk6qyhvHWzAxhCHVZfVOgfH5Aq9Dfsf980add0dZwGHa80add0rNq1ZF8Y8dGoRD5dbjzrNEJpbznXjg6IbYSbsrhWvKzzRdEhDgapXoe2L3tu1SwZ0add0LwPvLTfQL4HeEc6wr0add0hPO9OIboFy2oM0add0PS3wWhu0qixLwisnU0ciiDxEGBKbQ6gBvw8cZrDdr0slash0iKZDhkifNQfRZoJpWnUPJlROY3RageC2MdLi8JPuHdGwjYHA6lxD1YM42sXyeU9er730eNTizKkTpVAgbHKd5ppAWS50a4SwExX9q9uqxN3hXFbM7lC0OYk8Nku7XYm9P0add028fBrS7jq2cL9HBgBXnyeHGGbSWWvoUA49OUoZH2xGrdOOVcXJcgARsXJYzVZEm7r6wtfN0slash0h0slash0RtRyG2VCWs1rcTXLtPG01X7yIno5J0ZCFPxmPiIU3vOSE1slnzJrPyKkEqwa1zG02lykRfHt0slash060add0K924AdL8JdAn9VAjDDAFnBroZBlNavWrq6aZih2fcykA0uLnpcJvA4rxaEe3Ww5IKx9aXjcjE00slash0iISUvc8L0N80slash0upwTy88wgvtvQitRRpZIpEQ0equals00equals0'

def jpg_download(value, referer, path):
  """ download JPG via value generated by jpg_url_crawling """
  opener = urllib2.OpenerDirector()
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  req = urllib2.Request(_host+value['front'])
  req.add_header('Referer', _host+referer)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.1374.400')
  content = opener.open(req).read()
  ext = os.path.splitext(value['front'])
  no =  value['No.'].replace("/", "")
  with open(path + no +'a'+ext[1], "wb") as code:
    code.write(content)
  req = urllib2.Request(_host+value['back'])
  req.add_header('Referer', _host+referer)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 Safari/537.36 QQBrowser/8.0.1374.400')
  content = opener.open(req).read()
  with open(path + no +'b'+ext[1], "wb") as code:
    code.write(content)

def jpg_url_crawling(url):
  """ get jpg url and info from a JB page """
  opener = urllib2.OpenerDirector()
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  req = urllib2.Request(url)
  ct = opener.open(req).read()
  bs_page =  BeautifulSoup(ct)
  ele_url = bs_page.find_all('img')
  a = bs_page.find(text=u"\u7f16\u53f7")      # Number charactor
  b = a.find_next('td')                       # Number value
  c = a.parent
  d = c.find_next('tr')
  e = d.find_next('tr')
  f = e.find('td')
  t = list()
  for a in ele_url:
    if a.attrs['src'][1:7] == 'Upload':
      t.append(a.attrs['src'])
      h = a.find_next('br')
      c = h.find_next('br')
    # print ', '.join(['%s:%s' % item for item in b.__dict__.items()])
  val = dict()
  val['No.'] = b.contents[0]
  val['value'] = f.contents[0]
  val['type'] = f.find_next('td').contents[0]
  val['front'] = t[0]
  val['back'] = t[1]
  # print val
  return val

def jpg_page_crawling(url):
  """ get JB pages from a parent url """
  url_dict = dict()                                # declare a dictionary
  opener = urllib2.OpenerDirector()
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  req = urllib2.Request(url)
  req.add_data(_data)
  for (name, val) in _header.items():
    req.add_header(name, val)
  content = opener.open(req).read()
  bs_page =  BeautifulSoup(content)
  ul = bs_page.find('ul')                   # find first ul
  ind = 0
  while not ul is None:
    subind = 1
    li = ul.contents[subind]
    lista = list()
    while not li is None:
      subind = subind + 2
      lista.append(li.contents[1].attrs['href'])
      try:
        li = ul.contents[subind]
      except IndexError:
        break
    ul = ul.find_next('ul')                 # find next ul, use find_next method to update UL
    url_dict[str(ind)] = lista
    ind = ind + 1
    if ul is None:
      break
  for (index, suburl) in url_dict.items():
    print index,':',suburl
  return url_dict

def main():
  # test()
  # url_dict = jpg_page_crawling(_jb_url + str(_start))             # get dict
  # jb_dict = jpg_url_crawling(_host + url_dict['0'][0])
  # jpg_download(jb_dict, url_dict['0'][0], path)
  path = 'test/'
  # print jb_dict
  # return
  for i in range(_start, _end+1):
    url = _jb_url + str(i)
    fpath = path + str(i)
    if not os.path.exists(fpath):        # make directory
      os.makedirs(fpath)
    url_dict = jpg_page_crawling(url)             # get dict
    for (index, urllist) in url_dict.items():
      for jb_url in urllist:
        jb_dict = jpg_url_crawling(_host + jb_url)
        print 'fpath',fpath
        jpg_download(jb_dict, jb_url, fpath+'/')
  return
  opener = urllib2.OpenerDirector()
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  req = urllib2.Request('www.baidu.com')
  url_list = list()
  for i in range(_start, _end+1):
    # get url for every year
    url = _jb_url + str(i)
    req = urllib2.Request(url)
    req.add_data(_data)
    for (name, val) in _header.items():
      req.add_header(name, val)
    req.add_header('Refer', _refer+str(i))
    content = opener.open(req).read()
    # content = urllib2.urlopen(req).read()
    bs_page =  BeautifulSoup(content)
    print bs_page
    pic_url = bs_page.find_all('a')
    for a in pic_url:
      print a
      url_list.append(_host + a.attrs['href'])

    # download pic for every year
    for url in url_list:
      req = urllib2.Request(url)


if __name__ == '__main__':
  main()