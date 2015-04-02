
import urllib
import urllib2
import re
import sys
import gzip
import StringIO
import copy
import cookielib
import time

'''
  1. 打开登陆页面，获得用户名addr,vk,pwd
  2. 构造链接，POST数据
'''
_header_a = {
    u'Host':u'newlogin.sina.cn',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Referer':u'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=',
    u'Connection':u'keep-alive'
    }

class WBlogin():
    '''
      Expires: 设置的很早，保证每次登录都请求新的页面
      Cache-Control: no-cache不保存副本，must-revalidate必须重新验证
      Pragma: 不用管
      登陆首页: http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=
    '''

    def __init__(self, url=None, header=None, data=None, username=None, pwd=None):
        self.username = username
        self.url = url
        self.pwd = pwd
        self.header = header
        self.cookie_pool = list()      # 字典组成的列表，存储cookie信息字典name, value, expires, domain, data, httponly，只关心这6项
        self.cookie_ext = list()
        self.location = u''
        self.code = u''

    def login(self):
        '''
          登陆微博，返回账户基本信息
        '''
        #
        login_page = self.get_page(self.url, None, None)
        login_info = self.login_info_extractor(login_page)        # [addr, vk, pwd]
        print '-------open login page---------'
        print login_info
        print self.code

        # post count info
        # mobile
        # password_1406
        # remember

        # backURL : http%3A%2F%2Fweibo.cn%2F
        # backTitle : 微博
        # tryCount
        # vk : 1406_ef9c_1568546961
        # submit : 登陆
        # u'mobile=xinming_song%40sina.com&password_4285=14176596&backURL=http%253A%252F%252Fweibo.cn%252F&backTitle=%E5%BE%AE%E5%8D%9A&tryCount=&vk=4285_813c_1856403337&submit=%E7%99%BB%E5%BD%95'
        last_url = copy.copy(self.url)
        self.header['Referer'] = last_url
        self.url = u'http://login.weibo.cn/login/' + login_info[0]
        # 构造数据
        data = urllib.urlencode({'mobile':self.username, login_info[2]:self.pwd})
        data = data + '&backURL=http%253A%252F%252Fweibo.cn%252F' + '&backTitle=%E5%BE%AE%E5%8D%9A' + \
                        '&tryCount=' + '&vk=' + login_info[1] + '&submit=%E7%99%BB%E5%BD%95'
        times  = 0
        while True:       # 处理连续的302重定向
            print '-----------------start browser---------------'
            print self.url
            # for (name, nal) in self.header.items():
                # print name, ' : ',  nal
            # print self.header
            login_page = self.get_page(self.url, None, data)        # 获得网页，并且更新cookie
            print self.code
            if str(self.code) != u'302':
                break
            
            data = None
            # 处理头部
            self.header = _header_a
            # self.header['Referer'] = copy.copy(self.url)
            self.url = self.location
            pat = re.compile(u'(?<=://).+?(?=/)')
            if len(pat.findall(self.location)) > 0:
                host = pat.findall(self.location)
                self.header['Host'] = host[0]
                # print self.location
                # print host
            else:
                self.header['Host'] = ''
            # 分配cookie
            cookie_str = ''
            new_cookie = list()
            print 'loc: ' + self.location
            for i in self.cookie_pool:
                print i
            for i in self.cookie_pool:
                pos = self.header['Host'].find(i[2][1:])
                if pos > -1:
                   cookie_str += i[0] + '=' + i[1] + ';'
            
            if len(cookie_str) > 0:
                cookie_str = cookie_str[0:-1]
                
            self.header['Cookie'] = cookie_str
            if cookie_str == u'':
                del self.header['Cookie']
            
            times += 1
            print times
            # time.sleep(1)
        
        print login_page
        fn = open('done.txt', 'w+')
        fn.write(login_page)
        fn.close()
        print 'done'

    def cookie_analysis(self, cookie):
        '''
          cookie analysis
          cookie attrs : name, value, path, expires
        '''
        for i in cookie:
            existed = False
            for (index, j) in enumerate(self.cookie_pool):
                if j[0] == i.name.strip(u' ') and j[1] == i.domain.strip(u' '):
                  self.cookie_pool[index][1] = i.value.strip(u' ')
                  existed = True
                  break
            if existed is False:
                # self.cookie_pool.append([i.name.strip(u' '), i.value.strip(u' '), i.domain.strip(u' '), i.path.strip(u' ')])
                self.cookie_pool.append([i.name.strip(u' '), i.value.strip(u' '), i.domain.strip(u' ')])
        
        # print self.cookie_pool

    def get_page(self, url, header_in, data=None):
        if self.header == None:
            header = header_in
        else:
            header = self.header

        opener = urllib2.OpenerDirector()
        http_handler = urllib2.HTTPHandler()
        https_handler = urllib2.HTTPSHandler()
        cookie = cookielib.CookieJar()
        cookie_handle = urllib2.HTTPCookieProcessor(cookie)
        opener.add_handler(http_handler)
        opener.add_handler(https_handler)
        opener.add_handler(cookie_handle)
        req = urllib2.Request(url)
        for (name, val) in header.items():
            req.add_header(name, val)
        if data is not None:
            req.add_data(data)
            req.add_header(u'Content-Length', len(data))
        
        print 'trans header'
        for (name, nal) in self.header.items():
            print name, ': ',  nal
        print repr(data)
        try:
            r = opener.open(req, timeout = 60)
        except:
            print 'failed'
            opener.close()
            return False
        self.cookie_analysis(cookie)
        self.code = r.getcode()
        self.location = r.info().get('Location')
        # print r.info().get('Set-Cookie')
        # Make sure everything is working ;)
        if r.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO(r.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = r.read()

        return data

    def login_info_extractor(self, page):
        '''
          解析
        '''
        pg = page#.decode('utf-8')

        pat = re.compile(u'(?<=<form action=").+?(?=")')
        res = pat.findall(pg)
        if len(res) == 0:
            return False

        addr = self.htmldecoder(res[0])
        print addr

        pat = re.compile(u'(?<=name="vk" value=").+?(?=")')    # name="vk" value="3296_035e_1757547280"
        res = pat.findall(pg)
        if len(res) == 0:
            vk = ''
        else:
            vk = res[0]
        print vk

        pat = re.compile(u'(?<=type="password" name=").+?(?=")')    # type="password" name="password_3296"
        res = pat.findall(pg)
        if len(res) == 0:
            pwd = ''
        else:
            pwd = res[0]
        print pwd

        return [addr, vk, pwd]

    def htmldecoder(self, content):
        return content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '\"').replace("&#39;", '\'')









_header = {
    # u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Content-Type':u'application/x-www-form-urlencoded',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Referer':u'http://www.weibo.cn',
    u'Host':u'login.weibo.cn',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Connection':u'Keep-Alive'
    }

_data = u'mobile=xinming_song%40sina.com&password_4285=14176596&backURL=http%253A%252F%252Fweibo.cn%252F&backTitle=%E5%BE%AE%E5%8D%9A&tryCount=&vk=4285_813c_1856403337&submit=%E7%99%BB%E5%BD%95'

# mobile
# password_1406
# remember

# backURL : http%3A%2F%2Fweibo.cn%2F
# backTitle : 微博
# tryCount
# vk : 1406_ef9c_1568546961
# submit : 登陆
# _url = u'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
# _url = u'http://login.weibo.cn/?rand=944071466&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%E5%BE%AE%E5%8D%9A&vt=4&revalid=2&ns=1'
_url = u'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='       # 微博登陆页面地址





if __name__ == "__main__":
    # a = u'http:\\www.sina.com\sfsf\sd\a.index'
    # pat = re.compile(u'(?<=:\\\).+?(?=\\)')
    # print pat.findall(a)
    # sys.exit(0)
    a = WBlogin(_url, _header, None, 'xinming_song@sina.com', '14176596')
    a.login()
    # fn = open('login.txt', 'w+')
    # fn.write(page)pat = re.compile(u'(?<=://).+?(?=/)')
    # fn.close()
    # print page






