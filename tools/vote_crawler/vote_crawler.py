
# mk-button dark button-550ed3fe96c5b light-color  flat-dimension small pointed back-button

import urllib2
import gzip
import StringIO
import sys
import os
import re
import time
import random
from bs4 import BeautifulSoup


_header = {
    u'Host':u'chinabang.technode.com',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'*text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Connection':u'keep-alive'
  }


def get_urls(start_url):
    '''
      return urls of
    '''
    opener = urllib2.OpenerDirector()
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(start_url)
    for (name, val) in _header.items():
      req.add_header(name, val)
    # req.add_data(self.data)

    try:
        r = opener.open(req, timeout = 60)
    except:
        print 'failed'
        opener.close()
        r.close()
        sys.exit(0)
    # Make sure everything is working ;)
    if r.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(r.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = r.read()

    pat = re.compile(r'nominees/(.*)/"')
    result =  pat.findall(data)
    if result is None:
        print 'error'
    else:
        return result


def get_vote(url):
    '''
      get votes and name
    '''
    opener = urllib2.OpenerDirector()
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(url)
    for (name, val) in _header.items():
      req.add_header(name, val)

    try:
        r = opener.open(req, timeout = 60)
    except:
        print 'failed'
        opener.close()
        r.close()
        sys.exit(0)
    # Make sure everything is working ;)
    jump = r.info().get('Location')
    if jump is not None:
        req = urllib2.Request(jump)
        for (name, val) in _header.items():
            req.add_header(name, val)
        try:
            r = opener.open(req, timeout = 60)
        except:
            print 'failed'
            opener.close()
            r.close()
            sys.exit(0)

    if r.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(r.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = r.read()

    # print data
    page = BeautifulSoup(data)
    info = dict()
    ccc = page.find_all('span', attrs={'class':'dot-irecommendthis-count'})
    print ccc[0].get_text()
    if ccc is None:
        print data
        return None
    info['vote'] =  ccc[0].get_text()
    ccc = page.find_all('h1', attrs={'class':'page-introduce-title'})
    info['name'] =  ccc[0].get_text()
    return info



if __name__ == "__main__":
    # info = get_vote('http://chinabang.technode.com/nominees/themakers/')
    # info = get_vote('http://chinabang.technode.com/nominees/taidi/')
    # sys.exit(0)
    urls = get_urls('http://chinabang.technode.com/vote/')
    print urls
    fn = open(u'vote.csv', 'w+')
    index = 0;
    for a in urls:
        print index, ' of ', len(urls)
        url = 'http://chinabang.technode.com/nominees/' + a + '/'
        d = random.uniform(1, 6)
        time.sleep(int(d))
        info = get_vote(url)
        # print repr(info)
        if info is None:
            print 'failed'
            sys.exit(0)
        else:
            fn.write(info['vote']+',\n')
        index += 1
    fn.close()





# http://chinabang.technode.com/nominees/zengguanqing/
# http://chinabang.technode.com/nominees/helan/





