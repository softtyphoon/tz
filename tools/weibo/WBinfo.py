


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
from bs4 import BeautifulSoup



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
      fn = open('weibo.txt', 'w+')
      fn.write(page)
      fn.close()
      self.info_extractor(page)

    def info_extractor(self, page):
        '''
          提取信息
          【姓名】【所在城市】【标签】【人物简介】【博客地址】【人物资料】【关注数】【粉丝数】【微博数】【博文1内容|转发数|评论数|点赞数】【博文2内容|转发数|评论数|点赞数】【博文3内容|转发数|评论数|点赞数】
        '''
        page = page.decode('utf-8')
        # page = page.encode('utf-8')
        # print page
        # sys.exit(0)
        # 姓名
        pat = re.compile(u'(?<=<span class="ctt">).+?(?=&nbsp;)')
        res = pat.findall(page)
        if len(res) > 0:
            name = res[0].encode('gbk')
            print u'姓名：'.encode('gbk')+name

        # 城市

        # 标签

        # 人物介绍

        # 博客地址

        # 人物资料      ?
        # <a href="/1390399765/info?vt=4">资料</a>
        pat = re.compile(u'(?<=\<a href=")[^<]+?(?=">资料</a>)')
        res = pat.findall(page)
        info_url = u'http://weibo.cn' + res[0]
        self.url = info_url
        [area, tag, intr, blog] = self.account_info()
        print [area, tag, intr, blog]

        # 关注数
        pat = re.compile(u'(?<=关注\[)\d+?(?=\])')
        res = pat.findall(page)
        if len(res) > 0:
            follow = res[0].encode('gbk')
            print u'关注：'.encode('gbk')+follow

        # 粉丝数
        pat = re.compile(u'(?<=粉丝\[)\d+?(?=\])')
        res = pat.findall(page)
        if len(res) > 0:
            fans = res[0].encode('gbk')
            print u'粉丝：'.encode('gbk')+fans

        # 微博数
        pat = re.compile(u'(?<=微博\[)\d+?(?=\])')
        res = pat.findall(page)
        if len(res) > 0:
            weibo_num = res[0].encode('gbk')
            print u'微博数：'.encode('gbk')+weibo_num

        weibo = self.get_weibo(page)
        for i in weibo:
            for j in i:
                print j

    def account_info(self):
        '''
          地区，标签，人物介绍，博客地址
        '''
        page = self.get_page()
        page = page.decode('utf-8')

        # 地区
        pat = re.compile(u'(?<=地区:).+?(?=<br/>)', re.DOTALL)
        res = pat.findall(page)
        if len(res) == 0:
            area = u''
        else:
            area = res[0]
        
        # 标签
        pat = re.compile(u'(?<=标签:).+?(?=更多)', re.DOTALL)
        res = pat.findall(page)
        if len(res) == 0:
            tag = u''
        else:
            tag = self.html_tag_remove(res[0])
        
        # 人物介绍
        pat = re.compile(u'(?<=简介:).+?(?=<br/>)', re.DOTALL)
        res = pat.findall(page)
        if len(res) == 0:
            intr = u''
        else:
            intr = self.html_tag_remove(res[0])
            
        # 博客地址    没发现有这一项
        blog = u''
        
        return [area, tag, intr, blog]
        
        
    def favors_num(self, str):
        # print str
        pat = re.compile(u'(?<=赞\[).+?(?=\])', re.DOTALL)
        res = pat.findall(str)
        if len(res) == 0:
            favor = u''
        else:
            favor = res[0]

        pat = re.compile(u'(?<=转发\[)\d+?(?=\])', re.DOTALL)
        res = pat.findall(str)
        if len(res) == 0:
            forward = u''
        else:
            forward = res[0]

        pat = re.compile(u'(?<=评论\[)\d+?(?=\])', re.DOTALL)
        res = pat.findall(str)
        if len(res) == 0:
            comment = u''
        else:
            comment = res[0]

        # print [favor, forward, comment]
        return [favor, forward, comment]

    def get_weibo(self, page):
        '''
          提取最前面的三条微博
        '''
        weibo = list()
        pat = re.compile(u'(?<=<body>).+?(?=</body>)', re.DOTALL)
        # pat = re.compile(u'<body>.+</body>', re.DOTALL)
        res = pat.findall(page)
        body = res[0]

        pat = re.compile(u'(?<=class="c").+?(?=<div class="s">)', re.DOTALL)
        res = pat.findall(body)
        weibo_div = res

        count = 0
        for wb_div in weibo_div:
            # pat = re.compile(u'(?<=<div>).+?(?=</div>)', re.DOTALL)
            pat = re.compile(u'<div>.+?</div>', re.DOTALL)
            div_cell = pat.findall(wb_div)
            div_cnt = len(div_cell)

            weibo_content = ''
            favor = ''
            forward = ''
            comment = ''
            # 如果长度为1，则为无图发微博
            if div_cnt == 1:      #
                weibo_content = div_cell[0]
                weibo_content = self.html_tag_remove(weibo_content)
                index = weibo_content.find(u'赞[')
                weibo_content = weibo_content[0:index]
                [favor, forward, comment] = self.favors_num(weibo_content)

            # 如果长度为2，切第一个中找不到 转发了 字符，则为带图片发微博
            if div_cnt == 2:
                if div_cell[0].find('class="cmt"') == -1:
                    weibo_content = div_cell[0]
                    weibo_content = self.html_tag_remove(weibo_content)
                    [favor, forward, comment] = self.favors_num(div_cell[1])
                else:     # 否则为无图片转发
                    forward_a = self.html_tag_remove(div_cell[0])
                    forward_b = self.html_tag_remove(div_cell[1])
                    index = forward_b.find(u'赞[')
                    forward_b = forward_b[0:index]
                    [favor, forward, comment] = self.favors_num(div_cell[1])
                    weibo_content = forward_a + u'\n' + forward_b
                    
            if div_cnt == 3:    # 带图片转发
                forward_a = self.html_tag_remove(div_cell[0])
                forward_b = self.html_tag_remove(div_cell[2])
                index = forward_b.find(u'赞[')
                forward_b = forward_b[0:index]
                [favor, forward, comment] = self.favors_num(div_cell[2])
                weibo_content = forward_a + u'\n' + forward_b
                
                

            weibo_content = weibo_content.replace(u'&nbsp;', u' ')
            weibo.append([weibo_content, favor, forward, comment])
            count += 1
            if count == 3:
                break
        return weibo



            # if div_cnt == 2:      #


    def html_tag_remove(self, str):
        str = str.strip(u' ')
        str = str.strip(u'\n')
        # print str
        if str[0]!=u'<' or str[-1]!=u'>':
            print 'make sure the string is in a HTML format!'
            return False

        while True:
            indexl = str.find(u'<')
            indexr = str.find(u'>')
            if indexl == -1:
                break

            if indexr == -1:
                print 'make sure the string is in a HTML format!'
                return False

            if indexl == 0:
                if indexr == (len(str) - 1):
                    str = u''
                else:
                    str = str[indexr+1:]
                continue

            if indexr == (len(str) - 1):
                str = str[0:indexl]
                break

            str = str[0:indexl] + str[indexr+1:]

        return str


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
# _url = 'http://weibo.cn/FreedomKZ'# ?vt=4'

if __name__ == "__main__":
    # a = u'的地方[34]方式'
    # pat = re.compile(u'(?<=地方\[)\d+?(?=\])')
    # res = pat.findall(a)
    # res = pat.match(a)
    # print res.span(2)
    # print res
    # if len(res) > 0:
        # follow = res[0].decode('utf-8').encode('gbk')
        # print u'关注：'.encode('gbk')+follow
    # a = WBinfo(_url, _header, _cookie_str)
    # fn = open('weibo.txt', 'r+')
    # page=fn.read()
    # fn.close()
    # a.info_extractor(page)
    # sys.exit(0)

    a = WBinfo(_url, _header, _cookie_str)
    # a.account_info()
    a.get_info()




