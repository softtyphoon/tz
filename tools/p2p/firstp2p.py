#codng:utf-8
from bs4 import BeautifulSoup
import sys
import urllib2
import re

type = {
    'crd':u'产融贷',         # icon_melting
    'ysd':u'应收贷',         # icon_ysd'
    'a':u'd'
}






main_url = u'http://www.firstp2p.com/'
_header = {
    u'Host':u'www.firstp2p.com',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Referer':u'http://www.firstp2p.com/',
    u'Cookie':u'PHPSESSID=emk4jof8co8osccrrfao3vu0b0; _ncfdm=; _ncftr=; _ncf1=1427351222717.6764.0003.0002.0003.0002.0; _ncf2=1427351222717.8047.0003.0002; _ncf3=1427351254278.3.31561.6574.1.61744; mlta=%7B%22mltn%22%3A%7B%22250582%22%3A%5B%226729839450975941527%3E2%3E1427351254237%3E1%3E1427351254180%3E6729839450949563443%3E1427351228421%22%2C1442903254393%5D%7D%2C%22mlti%22%3A%7B%22250582%22%3A%5B%22142735122633671481%22%2C1442903226336%5D%7D%2C%22mltmapping%22%3A%7B%220%22%3A%5B1%2C1429943254395%5D%7D%2C%22mlts%22%3A%7B%22250582%22%3A%5B%225%22%2C1442903254334%5D%7D%7D; fpid=449038',
    u'Connection':u'keep-alive'
}


def get_primary_table(url = main_url, header = _header, data = None):
    opener = urllib2.OpenerDirector()
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(url)
    for (name, val) in header.items():
        req.add_header(name, val)
    if data is not None:
        req.add_data(self.data)

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

    # t = open('rer.txt', 'w+')
    # t.write(data)
    # t.close()
    # extract valid URLs
    fund_url = list()
    bs = BeautifulSoup(data)
    fund_div = bs.find_all('div', attrs={'id':'index_list_tab'})
    fund_div_s = fund_div[0].find_all('div', attrs={'class':'pro_name'})
    for a in fund_div_s:
      atag =  a.find('a')
      if atag is None:
          continue
      fund_url.append(atag['href'])
    return fund_url


def get_sub_table():
    return 0

if __name__ == "__main__":
    # fund_list = get_primary_table()
    # print repr(fund_list)
    # sys.exit(0)
    fn = open('rer.txt', 'r+')
    c = fn.read()
    bs = BeautifulSoup(c)
    fund_url = list()
    tbody = bs.find_all('tbody', attrs={'class':'j_index_tbody'})
    trs = tbody[0].find_all('tr')
    for tr in trs:
        atag =  tr.find('a')
        if atag is None:
            continue
        print atag['href']

        atag =  tr.find_all('div', attrs={'class':'pro_links'})
        str = atag[0].get_text()
        c = repr(str)
        pat = re.compile(r'(?<=1a).*(?=\\u4e07)')
        b = pat.findall(c)
        print b[0]

        
        atag =  tr.find_all('div', attrs={'class':'pl20'})
        text = atag[0].get_text().strip('\n')
        text = repr(text)
        pat = re.compile(r'')
        print repr(text) #.split('\n')
        
        # atag =  tr.find_all('em', attrs={'class':'color-yellow1'})
        # str = atag[0].get_text()
        # print str

        # t = atag[0].parent
        # print t
        # p = t.next_sibling
        # print p.string
        # print t.get_text()

    sys.exit(0)

    fund_div = bs.find_all('div', attrs={'id':'index_list_tab'})
    fund_div_s = fund_div[0].find_all('div', attrs={'class':'pro_name'})
    for a in fund_div_s:
      print repr(a)
      atag =  a.find('a')
      if atag is None:
          continue
      print atag['href']
      atag =  a.find_all('div', attrs={'class':'pro_links'})
      str = atag[0].get_text()
      c = repr(str)
      pat = re.compile(r'(?<=1a).*(?=\\u4e07)')
      b = pat.findall(c)
      print b[0]

      atag =  a.find_all('em', attrs={'class':'color-yellow1'})
      str = atag[0].get_text()
      # c = repr(str)
      # pat = re.compile(r'(?<=1a).*(?=\\u4e07)')
      # b = pat.findall(c)
      print str


    sys.exit(0)
    b = bs.find_all('div', attrs={'id':'index_list_tab'})
    # d = b[0].find_all('div', attrs={'class':'tc'})
    d = b[0].find_all('div', attrs={'class':'pro_name'})
    for a in d:
      # print a.contents[0].contents[0]
      atag =  a.find('a')
      if atag is None:
          continue
      print atag['href']
    print '+'


# total: tbody, j_index_tbody
# 可投金额：<em class="color-yellow1">737,682.86元</em>
# 总额：<div class="pro_links">
                                # 总额：100.00万
                                                                # <i class="badge"
      # atag =  a.find_all('div', attrs={'class':'pro_links'})
      # str = atag[0].get_text()
      # c = repr(str)
      # pat = re.compile(r'(?<=1a).*(?=\\u4e07)')
      # b = pat.findall(c)
      # print b[0]
# 剩余时间：<p>可投金额：<em class="color-yellow1">997,412.84元</em></p>
                            # <p>剩余时间：6天23时57分</p>

























