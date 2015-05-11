

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


# _url = 'http://newgame.17173.com/game-video-11958.html'
_url = 'http://tag.gamersky.com/v/2245.html'

video_src = {u'反恐精英OL2':'http://tag.gamersky.com/v/2245.html'}

_header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Connect':'keep-alive',
           'Accept-Encoding':'gzip, deflate'
          }

class video_spider(news_spider):
    def __init__(self, url=_url, header=_header, record ='', path=''):
        # super(video_spider, self).__init__(req_set[u'反恐精英OL2'], header, record)
        super(video_spider, self).__init__(url=url)
        self.url = url
        self.path = path
        self.header = header
        self.referer = u'gamersky.com'
        self.pic_path = self.path+u'视频缩略图\\'
        self.datasite = (u'youku',
                         u'bi',
                         u'17173',
                         u'tudou',
                         u'qq2',
                         u'ac',
                         )
        self.site = (u'http://static.youku.com/v/swf/loader.swf?VideoIDS=',
                     u'http://static.hdslb.com/miniloader.swf?aid=',
                     u'http://f.v.17173cdn.com/flash/PreloaderFileFirstpage.swf?cid=',
                     u'http://www.tudou.com/programs/view/html5embed.action?',
                     u'http://imgcache.qq.com/tencentvideo_v1/player/TencentPlayer.swf?vid=',
                     u'http://static.acfun.mm111.net/player/ACFlashPlayer.out.swf?type=page&url=http://www.acfun.tv/v/',
                     )
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
        url = self.url
        page_num = 0;
        while True:
            self.url = url
            page = ''
            page, cookie = self.get_page(url, self.header)
            pat = re.compile(u'(?<=charset=).+?(?=")', re.DOTALL)
            if page == '':
                continue
            res = pat.findall(page)
            if len(res) == 0:
                time.sleep(0.5)
                continue
            res = res[0]
            if 'utf-8' in res:
                page = page.decode('utf-8')
            elif 'gbk' in res or 'gb2312' in res:
                page = page.decode('gbk')

            # with open('t.txt', 'w+') as f:
                # f.write(page.encode('gbk'))

            pat = re.compile(u'(?<=<ul class="mw">).+?(?=</ul>)', re.DOTALL)
            res = pat.findall(page)
            if len(res) > 0:
                pat = re.compile(u'<li.+?</li>', re.DOTALL)
                res = pat.findall(res[0])
                for i in res:
                    print '.',
                    pat = re.compile(u'(?<=<a href=").+?(?=")', re.DOTALL)
                    res = pat.findall(i)
                    addr = res[0] if len(res) > 0 else ''
                    # print addr
                    addr = self.video_addr(addr)
                    if addr == None:
                        continue


                    referer = self.referer

                    pat = re.compile(u'(?<=<span>).+?(?=</span>)', re.DOTALL)
                    res = pat.findall(i)
                    date = res[-1][3:] if len(res) > 0 else ''
                    # print date

                    # pat = re.compile(u'(?<=>)[^<]+?(?=</span>)', re.DOTALL)
                    # res = pat.findall(i)
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

                    all = title + '|' + date + '|'
                    all += referer + '|'
                    all += pic_addr + '|'
                    all += addr + '\n'
                    # print all
                    self.fn.write(all.encode('utf-8'))
            # 判断是否还有下一页
            pat = re.compile(u'(?<=href=").+?(?=">下一页</a>)', re.DOTALL)
            res = pat.findall(page)
            if len(res) == 0:
                break
            else:
                url = res[0][len(res[0])-res[0][::-1].index('"'):]
                url = url.replace(u'&amp;', u'&')
                if not 'http://' in url:
                    url = 'http://' + urlparse.urlparse(self.start_url).netloc + url
                # print url
            page_num += 1
            if page_num == 1:
                # break
                pass
            delay = random.uniform(0.5, 2)
            time.sleep(delay)
            # print '.',
        print ''
        print u'视频信息爬取完成！！！'

    def video_addr(self, url):
        page = ''
        while page == '':
            page == ''
            page, cookie = self.get_page(url, self.header)
            if page == '':
                time.sleep(0.5)
                continue
            
            temp = page.lower()
            pat = re.compile(r'(?<=charset=).+?(?=")', re.DOTALL)
            res = pat.findall(temp)
            if len(res) == 0:
                continue
            res = res[0]
            if 'utf-8' in res:
                page = page.decode('utf-8')
            elif 'gbk' in res or 'gb2312' in res:
                page = page.decode('gbk')
            else:
                page = page.decode('utf-8')
            break
        if u'<title>无法找到页面</title>' in page:        # 实验发现，有的页面是无法打开的
            return None
        # with open('v.txt', 'w+') as f:
            # f.write(page.encode('gbk'))

        # data-sitename="youku" data-vid="XOTA5NjYxODE2"
        pat = re.compile(u'(?<=data-sitename=")[^"]+?(?=")', re.DOTALL)
        res = pat.findall(page)
        sitename = res[0] if len(res) > 0 else ''
        pat = re.compile(u'(?<=data-vid=").+?(?=")', re.DOTALL)
        res = pat.findall(page)
        video_id = res[0] if len(res) > 0 else ''
        # print sitename, video_id
        if u'iqiyi' in sitename:
            return video_id.replace(u'&amp;', '&')
        if sitename == '' and (u'sohu' in video_id):
            return video_id.replace(u'&amp;', '&')
        for (index, value) in enumerate(self.datasite):
            if sitename == value:
                if value == u'tudou':
                    url = self.site[index] + video_id.replace(u':', u'=')
                else:
                    url = self.site[index] + video_id
                return url.replace(u'&amp;', '&')
        # print url
        # print sitename
        # print video_id
        # print video_id
        # sys.exit(0)
        return None




if __name__ == "__main__":
    # path = u'c:\\视频\视频缩略图\\'
    # path = u'c:\\文档\\'
    # if not os.path.exists(path):
        # os.makedirs(path)
    # sys.exit(0)
    a = video_spider(path = u'c:\\视频\\')
    print a.video_addr(u'http://v.gamersky.com/201503/532126.shtml')
    pass


