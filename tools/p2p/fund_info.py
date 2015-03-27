

import urllib2
import re
import threading
import time



class fund_info(threading.Thread):
    def __init__(self, url=None, header=None, data=None):
        self.set_param(url, header, data)
        self.req_cookie = False         # relogin account
        self.hold = False               # wait for new cookie


    def set_param(self, url=None, header=None, data=None):
        self.url = url
        self.header = header
        self.data = data

    def get_page(self):
        '''
          得到页面
        '''
        print self.url
        opener = urllib2.OpenerDirector()
        http_handler = urllib2.HTTPHandler()
        https_handler = urllib2.HTTPSHandler()
        opener.add_handler(http_handler)
        opener.add_handler(https_handler)
        req = urllib2.Request(self.url)
        for (name, val) in self.header.items():
            req.add_header(name, val)
        if self.data is not None:
            req.add_data(self.data)

        try:
            r = opener.open(req, timeout = 60)
        except:
            print 'failed'
            opener.close()
            return False
        # Make sure everything is working ;)
        if r.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO(r.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = r.read()

        return data

    def get_status(self, page):
        '''
          依次返回：目前投资总额、剩余投资总额、剩余投资天数。
          返回格式：列表
          目前投资总额/剩余投资总额：精确到元
          剩余投资天数：以分钟表示
        '''
        info = list()
        pat = re.compile(r'(?<=<span class="color-yellow1 f16">)[\d\,\.]*(?=</span>)')
        r = pat.findall(page)
        if r is None:
            return False

        for a in r:
            c = int(float((a.replace(',', ''))))
            info.append(c)

        pat = re.compile(r'(?<=<span class="color-black f16">)[^<.*]*(?=</span>)', re.DOTALL)
        r = pat.findall(page)
        if r is not None:
            b = r[0].replace('\n', '')
            b = b.replace(' ', '')
            b = b.decode('utf-8').encode('gbk')
            # print b
            c = b
            # info.append(c)              # xx天xx时xx分
            c = c.replace('\xb7\xd6', "]")
            c = c.replace('\xca\xb1', ',')
            c = c.replace('\xcc\xec', ',')
            c = "["+c
            b = eval(c)
            min = 0
            for a in range(len(b)):
                min = min + b[-1-a]*(60**a)
            # print min, 'minites'
            info.append(min)
            return info

        info.append(None)
        return info

    def strategy():
        '''
          分析
        '''
        





































'''
    测试用例
'''
_url = 'http://www.firstp2p.com/deal/20337'
_header = {
    u'Host':u'www.firstp2p.com',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    # u'Referer':u'http://www.firstp2p.com/',
    # u'Cookie':u'PHPSESSID=emk4jof8co8osccrrfao3vu0b0; _ncfdm=; _ncftr=; _ncf1=1427351222717.6764.0003.0002.0003.0002.0; _ncf2=1427351222717.8047.0003.0002; _ncf3=1427351254278.3.31561.6574.1.61744; mlta=%7B%22mltn%22%3A%7B%22250582%22%3A%5B%226729839450975941527%3E2%3E1427351254237%3E1%3E1427351254180%3E6729839450949563443%3E1427351228421%22%2C1442903254393%5D%7D%2C%22mlti%22%3A%7B%22250582%22%3A%5B%22142735122633671481%22%2C1442903226336%5D%7D%2C%22mltmapping%22%3A%7B%220%22%3A%5B1%2C1429943254395%5D%7D%2C%22mlts%22%3A%7B%22250582%22%3A%5B%225%22%2C1442903254334%5D%7D%7D; fpid=449038',
    u'Cookie':u'_ncf1=1427281175480.2552.0042.0027.0004.0002.1; mlta=%7B%22mltn%22%3A%7B%22250582%22%3A%5B%226729839474450228134%3E2%3E1427374176901%3E1%3E1427374176932%3E4613147466355709634%3E1427281173830%22%2C1442926186803%5D%7D%2C%22mlti%22%3A%7B%22250582%22%3A%5B%22142728117549330967%22%2C1442833175493%5D%7D%2C%22mlts%22%3A%7B%22250582%22%3A%5B%225%22%2C1442833175698%5D%7D%2C%22mltmapping%22%3A%7B%220%22%3A%5B1%2C1429966186804%5D%7D%7D; __utma=11121699.127153641.1427288139.1427288139.1427288139.1; __utmz=11121699.1427288139.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ag_fid=jsATN6DIlyGFuiVF; __ag_cm_=1427288139015; _ga=GA1.2.127153641.1427288139; PHPSESSID=qc7nibvkktsbuaa0urguseou40; _ncfdm=; _ncftr=; _ncf2=1427370006554.8573.0004.0002; _ncf3=1427376214400.3.111752.110328.0.0',
    u'Connection':u'keep-alive'
}








if __name__ == "__main__":        # 用于测试
    c = fund_info(_url, _header)
    d = c.get_page()
    # d = True
    if d is False:
        print 'open page: %s --- failed' % (c.url)
    else:
        a = open('test1.txt', 'w+')
        a.write(d)
        # d = a.read()
        a.close()
        e = c.get_status(d)
        if e is not False:
            print repr(e)
        else:
            print 'parse page: %s --- failed' % (c.url)



































