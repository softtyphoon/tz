

import urllib2
import re
import multiprocessing
import time
import sys
import copy
from bs4 import BeautifulSoup


# class fund_info(threading.Thread):
class fund_info(object):
    def __init__(self, url=None, header=None, data=None, page=None, funds=None):
        self.set_param(url, header, data)
        self.req_cookie = False         # relogin account
        self.hold = False               # wait for new cookie
        self.page = page
        self.funds = funds
        self.no = 0
        self.banner = '编号,ID,姓,性别,投资金额,投资日期,投资时间,'

    def run(self):
        '''
          
        '''
        self.get_page()
        r = self.get_status()
        return r

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
            self.page = None
            return False
        # Make sure everything is working ;)
        if r.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO(r.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = r.read()

        self.page = data
        return data


    def get_primary(self):
        '''
          得到主表信息
            类型，
        '''
        page = self.page
        # 得到类型，名称
        pat = re.compile(r'(?<=\<title>).*(?=</title>)')
        catch = pat.search(page)
        # print catch.group().decode('utf-8').encode('gbk')
        catch = catch.group().decode('utf-8')#.encode('gbk')
        catch = catch.split(u'，')
        a = catch[0].split(u'-')
        b = catch[1].split(u'-')
        type = a[0]
        name = b[0]
        # print type, name

        # 得到编号
        pat = re.compile(r'/\d+')
        no = pat.findall(self.url)
        no = no[0][1:]
        self.no = no
        print self.url
        print no

        # 总额
        total = self.funds[1]

        # 年化收益率，期限
        profit = self.funds[6][0]
        date = self.funds[6][1]
        bonus = self.funds[6][2]
        bonus_name = self.funds[6][3]


        no2 = name.find('\d')
        # print no2
        return [no, type, name, no2, total, profit, date, bonus, bonus_name]

    def get_investor(self):
        '''
          得到投资人信息
          20150329：改为正则，BS解析有bug
        '''
        # fn = self.no + '.txt'
        # ppp = open(fn, 'w+')
        # ppp.write(self.page)
        # ppp.close()
        fn = self.no + '_info.txt'
        ppp = open(fn, 'w+')
        infos = list()
        page = self.page
        # print page
        pat = re.compile(r'(?<=<tbody>).+(?=</tbody>)', re.DOTALL)
        a = pat.findall(page)
        pat = re.compile(r'(?<=<tbody>).+', re.DOTALL)
        b = pat.findall(a[0])
        pat = re.compile(r'(?<=<tbody>).+', re.DOTALL)
        c = pat.findall(b[0])
        # print c
        # print len(c)
        # return 0
        tbody = c[0]
        ppp.write(tbody)
        ppp.write('\n')
        # pat = re.compile(r'(?<=\n)[0-9\\.]+(?=\n)')
        pat = re.compile(r'(?<=<span>)[^<]+(?=</span>)')
        namet =  pat.findall(tbody)
        # print namet
        # print len(str(namet))
        # return 0
        pat = re.compile(r'(?<=">)[^\n^<]+(?=</span>)')
        jine =  pat.findall(tbody)
        # print jine
        # print len(str(jine))
        # return 0
        pat = re.compile(r'(?<=<td>)[^<]+(?=</td>)')
        date =  pat.findall(tbody)
        # print date
        # print len((date))
        # return 0
        name = copy.copy(namet[1:])
        for (i, j) in enumerate(name):
            l = list()
            # print '--------------------------------'
            # print name[i].decode('utf-8')
            # print jine[i].decode('utf-8')
            # print date[i].decode('utf-8')
            a = name[i].decode('utf-8')
            # print a
            a = a.replace(u'（', ' ')
            a = a.replace(u'）', ' ')
            a = a.strip(u' ')
            p = a.split(u' ')
            # print p
            pp = p[1].decode('utf-8')
            l.append(p[0])      # id get
            l.append(pp[0])     # name get
            l.append(pp[1:])     # sex get
            a = jine[i].replace(u',', '')
            l.append(a)          # jine get
            a = date[i]
            a = a.split(' ')
            l.append(a[0])      # date get
            l.append(a[1])      # time get
            infos.append(l)
            # for lim in l:
                # lim = lim.encode('gbk')
                # ppp.write(lim)
            # ppp.write('\n')
        ppp.close()
        return infos

    def get_status(self):
        '''
          项目地址，投资总额，可投金额，剩余时间，可投金额差值，可投金额差值是否比上次的大(1)，[年化收益率，期限，收益方式，优惠]
          依次返回：目前投资总额、剩余投资总额、剩余投资天数。
          返回格式：列表
          目前投资总额/剩余投资总额：精确到元
          剩余投资天数：以分钟表示
        '''
        page = self.page
        # 是否需要重新登陆        URL=/user/login
        pat = re.compile(r'URL=/user/login')
        relogin = pat.findall(page)
        if len(relogin) != 0:
            print 'relogin please'
            return False
        primary_info = self.get_primary()         # 主表信息 
        # 不用重新登陆，提取信息
        fn = str(self.no)+'.csv'
        fund_file = open(fn, 'w+')
        # print self.banner
        a = self.banner
        a = a.decode('utf-8').encode('gbk')
        # fund_file.write('编号，ID，姓，性别，投资金额，投资日期，投资时间，')
        fund_file.write(a)
        fund_file.write('\n')
        info = self.get_investor()
        for l in info:
            fund_file.write(u'25698,')
            print l
            for ll in l:
                print ll
                # a = ll.decode('utf-8').encode('gbk')
                a = ll
                print a
                fund_file.write(a)
                fund_file.write(',')
            fund_file.write('\n')
        # try:
            # for l in info:
                # fund_file.write('25698,')
                # for ll in l:
                    # print ll
                    # a = ll.decode('utf-8').encode('gbk')
                    # fund_file.write(a)
                    # fund_file.write(',')
                # fund_file.write('\n')
        # except:
            # fund_file.close()
        fund_file.close()
        return primary_info         # 返回主表信息 

'''
    测试用例
'''
_url = 'http://www.firstp2p.com/deal/20572'
_header = {
    u'Host':u'www.firstp2p.com',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Referer':u'http://www.firstp2p.com/',
    # u'Cookie':u'PHPSESSID=emk4jof8co8osccrrfao3vu0b0; _ncfdm=; _ncftr=; _ncf1=1427351222717.6764.0003.0002.0003.0002.0; _ncf2=1427351222717.8047.0003.0002; _ncf3=1427351254278.3.31561.6574.1.61744; mlta=%7B%22mltn%22%3A%7B%22250582%22%3A%5B%226729839450975941527%3E2%3E1427351254237%3E1%3E1427351254180%3E6729839450949563443%3E1427351228421%22%2C1442903254393%5D%7D%2C%22mlti%22%3A%7B%22250582%22%3A%5B%22142735122633671481%22%2C1442903226336%5D%7D%2C%22mltmapping%22%3A%7B%220%22%3A%5B1%2C1429943254395%5D%7D%2C%22mlts%22%3A%7B%22250582%22%3A%5B%225%22%2C1442903254334%5D%7D%7D; fpid=449038',
    # u'Cookie':u'_ncf1=1427281175480.2552.0048.0029.0005.0002.3; mlta=%7B%22mltn%22%3A%7B%22250582%22%3A%5B%226720832428303710354%3E4%3E1427523712179%3E2%3E1427523712106%3E4613147466355709634%3E1427281173830%22%2C1443075723865%5D%7D%2C%22mlti%22%3A%7B%22250582%22%3A%5B%22142728117549330967%22%2C1442833175493%5D%7D%2C%22mlts%22%3A%7B%22250582%22%3A%5B%225%22%2C1442833175698%5D%7D%2C%22mltmapping%22%3A%7B%220%22%3A%5B1%2C1430115723867%5D%7D%7D; __utma=11121699.127153641.1427288139.1427288139.1427288139.1; __utmz=11121699.1427288139.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ag_fid=jsATN6DIlyGFuiVF; __ag_cm_=1427288139015; _ga=GA1.2.127153641.1427288139; PHPSESSID=10hcj6tcjjbagaagp5crjg0ga4; _ncfdm=; _ncftr=; _ncf2=1427523708979.2816.0003.0001; _ncf3=1427523723717.3.14738.9116.0.0; fpid=449038',
    u'Connection':u'keep-alive'
}




if __name__ == "__main__":        # 用于测试
    # a = open('data.txt', 'r+')
    # d = a.read()
    # a.close()
    # c = fund_info(_url, _header, None, d)
    # c.get_status()
    # sys.exit(0)
    funds = list(range(7))
    funds[6] = [0, 0, 0, 0]
    c = fund_info(_url, _header, None, None, funds)
    # d = c.get_page()
    # print d
    d = True
    if d is False:
        print 'open page: %s --- failed' % (c.url)
    else:
        # a = open('20582.txt', 'w+')
        # a.write(d)
        a = open('20518.txt', 'r+')
        d = a.read()
        a.close()
        c.page = d
        e = c.get_status()
        if e is not False:
            print repr(e)
        else:
            print 'parse page: %s --- failed' % (c.url)



































