

from news_spider import news_spider
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


_url = 'http://newgame.17173.com/game-video-11958.html'

video_src = {u'反恐精英OL2':'http://newgame.17173.com/game-video-11958.html'}

_header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Connect':'keep-alive',
           'Accept-Encoding':'gzip, deflate'
          }

class video_spider(news_spider):
    def __init__(self, req_set=video_src, header=_header, record ='', path=''):
        super(video_spider, self).__init__(req_set[u'反恐精英OL2'], header, record)
        self.req = req_set
        self.path = path
        self.header = header
        self.referer = u'17173'
        self.pic_path = self.path+u'视频缩略图\\'
        print self.pic_path
        if not os.path.exists(self.pic_path):
            os.makedirs(self.pic_path)
        self.fn = open(self.path + u'视频信息.txt', 'w+')

    def __del__(self):
        # super(video_spider, self).__del__()
        pass
        self.fn.close()

    def run(self):
        '''
          标题|时间|出处|缩略图地址|视频地址
        '''
        url = self.req[u'反恐精英OL2']
        page_num = 0;
        while True:
            page, cookie = self.get_page(url, self.header)
            pat = re.compile(u'(?<=charset=).+?(?=")', re.DOTALL)
            res = pat.findall(page)[0]
            if 'utf-8' in res:
                page = page.decode('utf-8')
            elif 'gbk' in res or 'gb2312' in res:
                page = page.decode('gbk')

            pat = re.compile(u'(?<=page-video-vlist">).+?(?=</ul>)', re.DOTALL)
            res = pat.findall(page)
            if len(res) > 0:
                pat = re.compile(u'<li.+?</li>', re.DOTALL)
                res = pat.findall(res[0])
                for i in res:
                    # print i
                    pat = re.compile(u'(?<=<a href=").+?(?=")', re.DOTALL)
                    res = pat.findall(i)
                    addr = res[0] if len(res) > 0 else ''
                    # print addr

                    referer = self.referer

                    pat = re.compile(u'(?<=</span>)[0-9\-]+?(?=</p>)', re.DOTALL)
                    res = pat.findall(i)
                    date = res[0] if len(res) > 0 else ''
                    # print date

                    pat = re.compile(u'(?<=>)[^<]+?(?=</span>)', re.DOTALL)
                    res = pat.findall(i)
                    title = res[0] if len(res) > 0 else ''
                    # print title

                    pat = re.compile(u'(?<=src=").+?(?=")', re.DOTALL)
                    res = pat.findall(i)
                    pic_addr = res[0] if len(res) > 0 else ''
                    # print pic_addr

                    # 下载图片
                    name = pic_addr[len(pic_addr)-pic_addr[::-1].index('/'):]
                    # print name
                    header = self.header
                    header['Referer'] = url
                    pic = ''
                    delay = 0
                    while pic == '':
                        time.sleep(delay)
                        pic, cookie = self.get_page(pic_addr, header_in=header)
                        delay = random.uniform(0.1, 0.5)

                    with open(self.pic_path + name, 'wb+') as f:
                        f.write(pic)

                    all = title + '  ' + date + '  '
                    all += referer + '  '
                    all += pic_addr + '  '
                    all += addr + '\n'
                    # print all
                    self.fn.write(all.encode('gbk'))
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
            page_num += 1
            if page_num == 2:
                # break
                pass
            delay = random.uniform(0.5, 2)
            time.sleep(delay)
            print '.',
        print ''
        print u'视频信息爬取完成！！！'







if __name__ == "__main__":
    # path = u'c:\\视频\视频缩略图\\'
    # path = u'c:\\文档\\'
    # if not os.path.exists(path):
        # os.makedirs(path)
    # sys.exit(0)
    a = video_spider(path = u'c:\\视频\\')
    a.run()
    pass


