
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
import copy
import zlib
import random
import urlparse



_header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Connection':'keep-alive',
           'Referer':'http://epub.sipo.gov.cn/gjcx.jsp',
           'Accept-Encoding':'gzip, deflate'
          }

_post_data = {'showType':'1',
              'strWord':u'',
              'numSortMethod':'',
              'strLicenseCode':'',
              'selected':'',
              'numFMGB':'',         # 发明公布
              'numFMSQ':'',         # 发明授权
              'numSYXX':'',         # 实用新型
              'numWGSQ':'',         # 外观设计
              'pageSize':'10',
              'pageNow':'1'
             }

html_space = ['&ensp;', '&nbsp;', '&emsp;', '&thinsp;']

_url = 'http://epub.sipo.gov.cn/patentoutline.action'

class patent_query():
    def __init__(self, header = _header, path=u'结果.csv'):
        self.header = _header
        self.post_data = ''
        self.url = _url
        self.cookie = None
        self.copcode = u'0'
        self.stcode = u'0'
        self.pa = u''
        self.types = ['fmgb', 'fmsq', 'xxsq', 'wgsq']
        self.type = ['numFMGB', 'numFMSQ', 'numSYXX', 'numWGSQ']
        self.type_chn = [u'发明公布', u'发明授权', u'实用新型', u'外观设计']
        if os.path.exists(path):
            self.fn = open(path, 'a')
        else:
            header_str = u'公司代码,股票代码,申请人,查询输出名字,专利类型,申请公布号/授权公告,申请号,申请公布日/授权公告日,申请日'
            self.fn = open(path, 'w')
            self.fn.write(header_str.encode('gbk'))
            self.fn.write('\n')

    def __del__(self):
        self.fn.close()

    def save2file(self, result):
        '''
          把结果写入到文件中
          result: [[], [], [], []]    依次为 发明公布, 发明授权, 实用新型, 外观设计
          [] 依次为 公布号 公布日 申请号 申请日 申请人
        '''
        for (index, val) in enumerate(result):
            if len(val) == 0:
                continue
            for i in val:
                content = u','.join([self.copcode, self.stcode, self.pa, i[4], self.type_chn[index], i[0], i[2], i[1], i[3]])
                self.fn.write(content.encode('gbk'))
                self.fn.write('\n')
                self.fn.flush()


    def run(self, pa=u'', copcode=u'0', stcode=u'0'):
        '''
          修改：修改由主查询界面直接查询，改为先获得专利信息，然后再分类查询，前者会造成很大的重复
        '''
        if pa == u'':
            print u'请输入申请人'
            return

        print u'开始处理：', copcode, stcode, pa
        self.pa = pa
        qword = u'申请（专利权）人=\'%' + pa + '%\''
        self.copcode = copcode
        self.stcode = stcode
        all_list = []
        patent_num = range(0, 4)

        # 预处理
        self.post_data = copy.copy(_post_data)
        self.post_data[self.type[0]] = '0'
        self.post_data[self.type[1]] = '0'
        self.post_data[self.type[2]] = '0'
        self.post_data[self.type[3]] = '0'
        self.post_data['pageNow'] = '1'
        self.post_data['strWord'] = qword.encode('utf-8')
        data = urllib.urlencode(self.post_data)
        page= ''
        while page == '':
            page, self.cookie = self.get_page(url_in=self.url, header_in=self.header, data=data, cookie_set=self.cookie)
            time.sleep(random.uniform(1.5, 2.5))
        # with open('www.txt', 'w+') as f:
            # f.write(page)
            # f.write(page.encode('gbk'))

        pat = re.compile(u'(?<=charset=).+?(?=")', re.DOTALL)
        res = pat.findall(page)[0]
        if 'utf-8' in res:
            page = page.decode('utf-8')
        elif 'gbk' in res or 'gb2312' in res:
            page = page.decode('gbk')
        else:
            page = page.decode('utf-8')

        pat_list = [u'(?<=发明公布：)\d+?(?=件)', u'(?<=发明授权：)\d+?(?=件)', u'(?<=实用新型：)\d+?(?=件)', u'(?<=外观设计：)\d+?(?=件)']
        for (index, i) in enumerate(pat_list):
            pat = re.compile(i)
            res = pat.findall(page)
            if len(res) == 0:
                patent_num[index] = '0'
            else:
                patent_num[index] = res[0]

        # print patent_num
        # sys.exit(0)
        # 开始进行具体专利信息爬取
        for (index, i) in enumerate(self.types):
            this_list = []
            pagenum = 1
            while True:     # 一直翻页，直到没有下一页为止
                if patent_num[index] == '0':
                    print self.type_chn[index], u'在本项目下没有专利'
                    break
                else:
                    # 构造数据
                    self.post_data = copy.copy(_post_data)
                    self.post_data[self.type[0]] = patent_num[0]
                    self.post_data[self.type[1]] = patent_num[1]
                    self.post_data[self.type[2]] = patent_num[2]
                    self.post_data[self.type[3]] = patent_num[3]
                    self.post_data['selected'] = i
                    self.post_data['pageNow'] = str(pagenum)
                    self.post_data['strWord'] = qword.encode('utf-8')
                    # print self.post_data
                    data = urllib.urlencode(self.post_data)
                    print u'类型:', self.type_chn[index], u'页数:', pagenum, u'数量:', patent_num[index]
                    page= ''
                    while page == '':
                        # print self.url, data
                        page, self.cookie = self.get_page(url_in=self.url, header_in=self.header, data=data, cookie_set=self.cookie)
                        time.sleep(random.uniform(1.5, 2.5))

                    pat = re.compile(u'(?<=charset=).+?(?=")', re.DOTALL)
                    res = pat.findall(page)[0]
                    if 'utf-8' in res:
                        page = page.decode('utf-8')
                    elif 'gbk' in res or 'gb2312' in res:
                        page = page.decode('gbk')

                    # with open('test.txt', 'w+') as f:
                        # f.write(page.encode('gbk'))

                    this_list += self.info_extractor(page)
                    pat = re.compile(u'(?<=<a).+?(?=>&gt;</a>)', re.DOTALL)
                    res = pat.findall(page)
                    if len(res) == 0:
                        break
                    # else:
                        # print 'go to next page'
                    # time.sleep(random.uniform(1.5, 2.5))
                    pagenum += 1
                    del self.post_data
            all_list.append(this_list)

        return all_list


    def info_extractor(self, page):
        '''
          提取信息，得到 [专利权人，公布号(授权公布号)，申请号，申请公布日/授权公告日，申请日]
          1. 取出标签；html解码 &ensp;
        '''
        non = u'抱歉，没有您要查询的结果'
        if non in page:
            with open('test.txt', 'w+') as f:
                f.write(page.encode('gbk'))
            print u'>>>>>>该项目下没有专利'
            return []
        info = []
        pat_list = [u'(?<=<div class="cp_linr">).+?(?=<div class="cp_jsh">)']
        for pat in pat_list:
            pat = re.compile(pat, re.DOTALL)
            res = pat.findall(page)
            if len(res) > 0:
                break

        if len(res) == 0:
            print u'Add new pattern'
            sys.exit(0)

        for i in res:
            # 公布号 公布日 申请号 申请日 申请人
            pat = re.compile(u'(?<=：).+?(?=</li>)', re.DOTALL)
            cont = pat.findall(i)
            for k in range(0, 5):
                cont[k] = self.html_tag_remove(cont[k])
                if cont[k].find(';') > -1:
                    cont[k] = cont[k][0:cont[k].find(';')]

            info.append(cont[0:5])
            # print cont[0:5]
            # for i in cont:
                # print i,
            # print ''      <a href="javascript:zl_fy(2);">&gt;</a>
        return info

    def html_tag_remove(self, str):
        '''
          通用方法，移除tag
        '''
        pat = re.compile(u'<.+?>', re.DOTALL)
        res = pat.findall(str)
        str_fix = str
        for i in res:
            str_fix = str_fix.replace(i, ' ')

        for i in html_space:
            str_fix = str_fix.replace(i, ' ')
        return str_fix


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
            req.add_header(u'Content-Type', 'application/x-www-form-urlencoded')

        try:
            time_format = '%Y-%m-%d %X'
            # print time.strftime(time_format, time.localtime())
            r = ''
            r = opener.open(req, timeout = 45)
            # Make sure everything is working ;
            print r.info().get('Content-Length')
            if r.info().get('Transfer-Encoding') == 'chunked':
                # print 'chunked'
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
            if r != '':
                r.close()
            opener.close()
            sys.exit(0)
        except:
            data = ''
            time_format = '%Y-%m-%d %X'
            # print time.strftime(time_format, time.localtime())
            print 'Time Out'
        finally:
            if r != '':
                r.close()
            opener.close()

        return [data, cookie]

if __name__ == "__main__":
    word = u'万科企业股份有限公司'
    word = u'中兴通讯股份有限公司'
    # with open('test.txt', 'r') as f:
        # page = f.read()
    a = patent_query()
    result = a.run(word)
    a.save2file(result)
    # a.info_extractor(page.decode('gbk'))


