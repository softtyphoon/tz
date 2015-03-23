

import urllib2
import gzip
import csv
import re
import sys
import random
import time
from StringIO import StringIO
from bs4 import BeautifulSoup

class GTcsvdownloader():
  '''
  downloader csv file from www.google.com/trends
  '''

  def __init__(self, key_word=None):
    self.header = {
        u'Host':u'nba.hupu.com',
        u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
        u'Accept':u'*/*',
        u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        u'Accept-Encoding':u'gzip, deflate',
        u'X-Requested-With':u'XMLHttpRequest',
        u'Referer':u'http://nba.hupu.com/',
        u'Cookie':u'__gads=ID=2b2bd8ba9623de18:T=1426753963:S=ALNI_MZ1bA2TFh-2pDQ6UpeAXFOTyirSAA',
        u'Connection':u'keep-alive'
      }
    self.name = key_word
    self.timeout = 60
    self.data = u'username=03575&password=sxm223.'
    # self.url = u'https://www.baidu.com/home/xman/data/xcardhtml?cardid=6&&_req_seqid=0xdaf0a11f0009353e&asyn=1&t=1426555419570&sid='
    self.url = u'http://nba.hupu.com/boxscore/boxscore.php'

  def get_csv(self):
    '''
    messy code solution: b.decode('utf-8').encode('gbk')
    '''
    opener = urllib2.OpenerDirector()
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(self.url)
    for (name, val) in self.header.items():
      req.add_header(name, val)

    # req.add_data(self.data)
    try:
      r = opener.open(req, timeout = self.timeout)
    except:
      print 'failed'
      opener.close()
      r.close()
      sys.exit(0)
    # Make sure everything is working ;)
    if r.info().get('Content-Encoding') == 'gzip':
      buf = StringIO(r.read())
      f = gzip.GzipFile(fileobj=buf)
      data = f.read()
    else:
      data = r.read()
    page = eval(data)
    print page['html']
    # print data
    # print dict(data)
    # print page['html']
    # print BeautifulSoup(page['html'])

if __name__ == '__main__':
  a = GTcsvdownloader()
  c = a.get_csv()



