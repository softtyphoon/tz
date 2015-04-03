


import urllib
import urllib2
import re
import sys
import gzip
import StringIO
import copy
import cookielib
import time
import argparse



class WBinfo():
    def __init__(self, url, header, cookie_str):
        '''
          初始化
        '''
        self.url = url                        # 爬取的微博url
        self.header = header
        self.cookie_str = cookie_str

    def get_info(self):
      '''
        得到感兴趣的内容
        【姓名】【所在城市】【标签】【人物简介】【博客地址】【人物资料】【关注数】【粉丝数】【微博数】【博文1内容|转发数|评论数|点赞数】【博文2内容|转发数|评论数|点赞数】【博文3内容|转发数|评论数|点赞数】
      '''
      self.header['Cookie'] = self.cookie_str
      page = self.get_page()
      # fn = open('weibo.txt', 'w+')
      # fn.write(page)
      # fn.close()
      self.info_extractor(page)

    def info_extractor(self, page):
        '''
          提取信息
          【姓名】【所在城市】【标签】【人物简介】【博客地址】【人物资料】【关注数】【粉丝数】【微博数】【博文1内容|转发数|评论数|点赞数】【博文2内容|转发数|评论数|点赞数】【博文3内容|转发数|评论数|点赞数】
        '''

        # 姓名
        pat = re.compile(u'(?<=<span class="ctt">).+?(?=&nbsp;)')
        res = pat.findall(page)
        if len(res) > 0:
            name = res[0].decode('utf-8').encode('gbk')
            print u'姓名：'.encode('gbk')+name

        # 城市

        # 标签

        # 任务介绍

        # 博客地址

        # 人物资料      ?

        # 关注数
        pat = re.compile(r'(?<=关注\[)\d+?(?=\])')
        res = pat.findall(page)
        if len(res) > 0:
            follow = res[0].decode('utf-8').encode('gbk')
            print u'关注：'.encode('gbk')+follow

        # 粉丝数
        pat = re.compile(r'(?<=粉丝\[)\d+?(?=\])')
        res = pat.findall(page)
        if len(res) > 0:
            fans = res[0].decode('utf-8').encode('gbk')
            print u'粉丝：'.encode('gbk')+fans

        # 微博数
        pat = re.compile(r'(?<=微博\[)\d+?(?=\])')
        res = pat.findall(page)
        if len(res) > 0:
            weibo_num = res[0].decode('utf-8').encode('gbk')
            print u'微博数：'.encode('gbk')+weibo_num



    def get_page(self):
        '''
          得到指定页面的内容
        '''
        header = self.header
        url = self.url
        data = None

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

        # print 'trans header'
        # for (name, nal) in self.header.items():
            # print name, ': ',  nal
        # print repr(data)
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

_cookie_str = u'_T_WM=1b82c71e02e718c24d6dcc30662034c1;SUB=_2A254GsV0DeTxGeVP4lsW8i_PyjiIHXVb5Os8rDV6PUJbrdANLW3akW2RAo7sJklaf2niOM5QDo02aaSijw..;gsid_CTandWM=4u8Bdba21IvHA1duEEqs5dqop54'

_header = {
    u'Host':u'weibo.cn',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Connection':u'keep-alive'
    }

_url = 'http://weibo.cn/lqszjx'# ?vt=4'

if __name__ == "__main__":
    # a = u'的地方[34]方式'
    # pat = re.compile(u'(?<=地方\[)\d+?(?=\])')
    # res = pat.findall(a)
    # print res
    # if len(res) > 0:
        # follow = res[0].decode('utf-8').encode('gbk')
        # print u'关注：'.encode('gbk')+follow

    # sys.exit(0)

    a = WBinfo(_url, _header, _cookie_str)
    a.get_info()




