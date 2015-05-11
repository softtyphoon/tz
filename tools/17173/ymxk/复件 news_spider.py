

import urllib
import urllib2
import cookielib
import time
import StringIO
import gzip
import sys
import re
import time
import os
import zlib
import random
import urlparse

_spec_char = [u'\\', u'/', u'*', u'|', u'<', u'>', u'?', u':', u'"']

_header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Connect':'keep-alive',
           'Accept-Encoding':'gzip, deflate'
          }

_url = 'http://newgame.17173.com/game-newslist-11958.html?news_type=1'

class news_spider(object):
    def __init__(self, url=_url, header=_header, start_title = '', path = ''):
        self.start_url = url
        self.start_title = start_title          # 用于断点下载
        self.header = header
        self.referer = u'17173.com'
        self.path = path
        self.fileid = '00000000000000000'
        if not path == '':
            if not os.path.exists(self.path):
                os.makedirs(self.path)

            if not os.path.exists(self.path + u'图片\\'):
                os.makedirs(self.path + u'图片\\')
        pass

    def __del__(self):
        # self.record.close()
        pass

    def run(self):
        '''
          进行新闻爬取
        '''
        # 打开主页
        url = self.start_url
        while True:
            page, cookie = self.get_page(url, self.header)
            # with open('t.txt', 'w+') as f:
                # f.write(page)
            # with open('t.txt', 'r') as f:
                # page = f.read()
            pat = re.compile(u'(?<=charset=).+?(?=")', re.DOTALL)
            res = pat.findall(page)[0]
            if 'utf-8' in res:
                page = page.decode('utf-8')
            elif 'gbk' in res or 'gb2312' in res:
                page = page.decode('gbk')

            # 解析网页    [日期，名称，url]
            news_set = self.src_web_analysis(page)

            # 新闻下载
            for i in news_set:
                delay = random.uniform(1.5, 2.5)
                time.sleep(delay)
                self.news_download(i[2], i[1], i[0])

           # 判断是否还有下一页
            pat = re.compile(u'(?<=class="next").+?(?=下一页</a>)', re.DOTALL)
            res = pat.findall(page)
            if len(res) == 0:
                break
            else:
                pat = re.compile(u'(?<=href=").+?(?=">)', re.DOTALL)
                res = pat.findall(res[0])[0].replace(u'&amp;', u'&')
                url = res
                if not 'http://' in url:
                    url = 'http://' + urlparse.urlparse(self.start_url).netloc + url


    def news_download(self, url, title, date):
        '''
          下载新闻及其图片
          传入参数：url，新闻的网址
        '''
        # print u'下载新闻：', title, url
        print '.',
        trail = url[len(url)-1-url[::-1].index('.'):]
        all = u'_all' + trail
        trail = u'_1' + trail
        if trail in url:
            url = url.replace(trail, all)

        # print url
        page = ''
        delay = 0
        rty = 0
        while page == '':
            rty += 1
            time.sleep(delay)
            page, cookie = self.get_page(url, self.header)
            delay = random.uniform(0.5, 2)
            if rty == 10:
                return

        # with open('news.txt', 'w+') as f:
            # page = f.read()
            # f.write(page)

        page = page.lower()
        pat = re.compile(u'(?<=charset=).+?(?=")', re.DOTALL)
        res = pat.findall(page)[0]
        if 'utf-8' in res:
            try:
              page = page.decode('utf-8')
            except:
              page = page.decode('gbk')
        elif 'gbk' in res or 'gb2312' in res:
            page = page.decode('gbk')

        res = self.content_extractor(page)
        # with open('xxx.txt', 'w+') as f:
            # f.write(res.encode('gbk'))
        # t = self.get_time()
        # if t == self.fileid[0:14]:
            # index = int(self.fileid[14:]) + 1
            # index = str(index)
            # if len(index) == 1:
                # self.fileid[-1] = index
            # if len(index) == 2:
                # self.fileid[-2:] = index
            # if len(index) == 3:
                # self.fileid[-3:] = index
        # else:
            # self.fileid = (t + '000')

        header = title + '|' + date + '|' + self.referer + '\n'
        self.fileid = title + '_' + date
        for i in _spec_char:
            self.fileid = self.fileid.replace(i, u'')
        with open(self.path + self.fileid + u'.txt', 'w+') as f:
            f.write(header.encode('gbk'))
            f.write(self.content_process(res, url))

    def content_extractor(self, page):
        '''
          提取咨询内容，并过滤掉视频
        '''
        over = False
        pat_list = [u'<div class="gb-final-mod-article".+?</div>', u'<div class="article-con".+?</div>', u'<div class="art-con".+?</div>']
        video_pat = [u'<div class="video-box">.+?</div>']
        while not over:
            for i in pat_list:
                pat = re.compile(i, re.DOTALL)
                res = pat.findall(page)
                if len(res) > 0:
                    break
            if len(res) == 0:
                return ''

            # 剔除视频
            for i in video_pat:
                pat = re.compile(i, re.DOTALL)
                video = pat.findall(res[0])
                if len(video) > 0:
                    # print video[0]
                    pat = re.compile(u'(?<=src=").+?(?=")', re.DOTALL)
                    video_url = pat.findall(video[0])[0]
                    # print video_url
                    video_url = '\n' + video_url + '\n'
                    page = page.replace(video[0], video_url)
                    break
                over = True
        return res[0]


    def src_web_analysis(self, page):
        '''
          从源网站获取新闻信息
          返回新闻的 [日期，名称，url]
        '''

        # with open('1.txt', 'r') as f:
            # f.write(page)
            # page = f.read()

        info = []
        pat = re.compile(u'<div class="article-list">.+?</div>', re.DOTALL)
        res = pat.findall(page)[0]

        pat = re.compile(u'<li>.+?</li>', re.DOTALL)
        res = pat.findall(res)
        for i in res:
            # print i
            pat = re.compile(u'(?<=<span class="date">).+?(?=</span>)', re.DOTALL)
            date = pat.search(i).group().strip()

            title = self.html_tag_remove(i).replace(date, '').strip()
            url = ''
            pat = re.compile(u'(?<=href=").+?(?=")', re.DOTALL)
            url = pat.findall(i)[0]
            info.append([date, title, url])
        return info

    def content_process(self, strs, url):
        '''
          通用方法，移除tag
        '''
        # 针对某些网页，先进行一遍过滤
        pat = re.compile(u'<img.+?>', re.DOTALL)
        res = pat.findall(strs)
        str_fix = strs
        for i in res:
            if '<' in i[1:]:
                str_fix = str_fix.replace(i[i[1:].index('<')+1:], '')

        # print str_fix
        pat = re.compile(u'<.+?>', re.DOTALL)
        res = pat.findall(str_fix)
        for i in res:
            if '<img' in i or '<IMG' in i:
                # print i
                pat = re.compile(u'(?<=src=").+?(?=")', re.DOTALL)
                res = pat.findall(i)
                if len(res) > 0:
                    res = res[0]
                    name = res[len(res)-res[::-1].index('/'):]
                    rstr = name
                    # 下载图片
                    header = self.header
                    header['Referer'] = url
                    page = ''
                    delay = 0
                    while page == '':
                        time.sleep(delay)
                        page, cookie = self.get_page(res, header_in=header)
                        delay = random.uniform(0.5, 2)

                    with open(self.path + u'图片\\'+name, 'wb+') as f:
                        f.write(page)
            elif '<br>' == i:
                rstr = '\n'
            else:
                rstr = ''
            str_fix = str_fix.replace(i, rstr)
        return str_fix.encode('gbk')

    def html_tag_remove(self, str):
        '''
          通用方法，移除tag
        '''
        pat = re.compile(u'<.+?>', re.DOTALL)
        res = pat.findall(str)
        str_fix = str
        for i in res:
            str_fix = str_fix.replace(i, ' ')
        return str_fix

    def get_time(self):
        time_set = time.localtime(time.time())
        year = str(time_set.tm_year)
        month = str(time_set.tm_mon)
        day = str(time_set.tm_mday)
        hour = str(time_set.tm_hour)
        min = str(time_set.tm_min)
        sec = str(time_set.tm_sec)
        month = ('0'+month) if len(month) == 1 else month
        day = ('0'+day) if len(day) == 1 else day
        hour = ('0'+hour) if len(hour) == 1 else hour
        sec = ('0'+sec) if len(sec) == 1 else sec
        min = ('0'+min) if len(min) == 1 else min
        return year + month + day + hour + min + sec

    def get_page(self, url_in=None, header_in=None, data=None, cookie_set=None):
        '''
          通用方法，请求页面
        '''
        url = url_in
        header = header_in
        header['Host'] = urlparse.urlparse(url).netloc

        opener = urllib2.OpenerDirector()
        http_handler = urllib2.HTTPHandler()
        https_handler = urllib2.HTTPSHandler()

        if cookie_set == None:
            cookie = cookielib.CookieJar()
        else:
            cookie = cookie_set

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

        try:
            r = ''
            r = opener.open(req, timeout = 30)
            # Make sure everything is working ;
            if r.info().get('Transfer-Encoding') == 'chunked':
                d = zlib.decompressobj(16+zlib.MAX_WBITS)
                content = ''
                while True:
                    data = r.read()
                    if not data:
                      break
                    content += d.decompress(data)
                data = content
            else:
                if r.info().get('Content-Encoding') == 'gzip':
                    buf = StringIO.StringIO(r.read())
                    f = gzip.GzipFile(fileobj=buf)
                    data = f.read()
                else:
                    data = r.read()
        except KeyboardInterrupt:
            print 'EXIT: Keyboard Interrupt'
            sys.exit(0)
        except:
            data = ''
            # print 'Time Out'
        finally:
            if r != '':
                r.close()
            opener.close()

        return [data, cookie]







if __name__ == "__main__":
    # a = 'http://wdsf.dsdf.sdf/sda/sdfdg.jpg'
    # print a[len(a)-a[::-1].index('.')-1:]
    # print urlparse.urlparse(a)
    # if os.path.exists('pic'):
        # os.mkdir('aaa')
    # print os.path()
    # print time.localtime(time.time())
    # sys.exit(0)
    a = news_spider(path=u'c:\新闻\\')
    # a.get_time()
    a.run()
    # a.news_download(u'http://news.17173.com/yzyy/2014/49/5/index.shtml', 'test')
    # a.src_web_analysis()
    # a = 'http://ssffd.csf.com/sdsf/saf.php'
    # print urlparse.urlparse(a).netloc
    pass


