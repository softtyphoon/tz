﻿


import urllib
import urllib2
import re
import sys
import gzip
import StringIO
import copy
import cookielib
import time
import random
import argparse
# from bs4 import BeautifulSoup



class WBinfo():
    def __init__(self, url, header, cookie_str, depth=0, db_set = [None, None]):
        '''
          初始化
          数据库格式：depth varchar(20),name varchar(20), area varchar(20), url varchar(50)
        '''
        self.url = url                        # 爬取的微博url
        self.header = header
        self.cookie_str = cookie_str
        self.header['Cookie'] = self.cookie_str
        self.fans_list = []
        self.depth_set = depth
        self.db = db_set[0]
        self.db_table = db_set[1]

    def wb_sn(self, url, depth):
        '''
          得到微博之间的关系
        '''
        pass

    def sn_info(self, url):
        '''
          得到账号信息，以及粉丝
          返回格式 [[name, area, url], [[name, url], [name, url], ...]]
        '''
        page_num = 2
        info = []
        while True:
            delay = random.uniform(1, 3)
            time.sleep(delay)
            page = self.get_page(url)
            if page:
                break

        # 得到博主的信息
        pat = re.compile(u'(?<=\<a href=")[^<]+?(?=">资料</a>)')
        res = pat.findall(page)
        info_url = u'http://weibo.cn' + res[0]
        self.url = info_url
        area, tag, intr, name = self.account_info()

        info.append([name, area, url])

        # 得到粉丝
        pat = re.compile(u'(?<=粉丝\[).+?(?=\])')
        res = pat.findall(page)
        if res[0] == u'0':    # 没有粉丝
            return info

        # 进入粉丝页，查找粉丝
        pat = re.compile(u'(?<=href=")[^<]+?(?=">粉丝\[)')
        res = pat.findall(page)
        url = u'http://weibo.cn' + res[0]
        fan_list = self.retrive_fans(url, page_num)
        info.append(fan_list)       # 传入主页的信息以及粉丝情况
        return info

    def all_info(self, url=None):
        '''
          返回微博的 关注数，粉丝数，地区
        '''
        page = self.get_page(urlin=url)
        # with open('1.txt', 'w+') as f:
            # f.write(page.encode('utf-8'))
        # with open('1.txt', 'r') as f:
            # page=f.read()
        

        follow = ''
        pat = re.compile(u'(?<=关注\[)\d+?(?=\])')
        res = pat.findall(page)
        # print res
        if len(res) > 0:
            follow = res[0].decode('utf-8').encode('gbk')

        fans = ''
        pat = re.compile(u'(?<=粉丝\[)\d+?(?=\])')
        res = pat.findall(page)
        # print res
        if len(res) > 0:
            fans = res[0].decode('utf-8').encode('gbk')

        pat = re.compile(u'(?<=\<a href=")[^<]+?(?=">资料</a>)')
        res = pat.findall(page)
        info_url = u'http://weibo.cn' + res[0]
        self.url = info_url
        # print info_url
        area, tag, intr, name = self.account_info()

        # print 'f:', follow, 'fans', fans, 'area', area
        return [follow, fans, area]
        pass

    def sn_analysis(self, url):
        '''
          社交网络关系分析
          数据来源 : b = a.sn_info(_url)     # [[name, area, url], [[name, url], [name, url], ...]]
        '''
        # 首先得到入口微博以及其粉丝的信息
        all_sn = list()
        main_info = self.sn_info(url)
        all_sn.append(main_info)
        print main_info[0][0], main_info[0][1], main_info[0][2]
        for j in main_info[1][:]:
            print j[0], j[1]
        print ''
        if self.db is not None:         # 写入数据库   name area url
            [follow, fans, area] = self.all_info(main_info[0][2])
            cur = self.db.cursor()
            db_name = main_info[0][0].encode('utf-8')
            db_area = main_info[0][1].encode('utf-8')
            db_url = main_info[0][2].encode('utf-8')
            db_follow = follow.encode('utf-8')
            db_fans = fans.encode('utf-8')
            statement = "insert into %s value('%s', '%s', '%s', '%s', '%s')" % ('all_sn', db_name, db_area, db_url, db_follow, db_fans)
            cur.execute(statement)
            cur.close()
            self.db.commit()

        # 然后再得到粉丝微博的信息以及其各自的粉丝
        for i in main_info[1][:]:
            info = self.sn_info(i[1])
            all_sn.append(info)
            print info[0][0], info[0][1], info[0][2]
            for j in info[1][:]:
                print j[0], j[1]
            # 写入数据库
            [follow, fans, area] = self.all_info(info[0][2])
            cur = self.db.cursor()
            db_name = info[0][0].encode('utf-8')
            db_area = info[0][1].encode('utf-8')
            db_url = info[0][2].encode('utf-8')
            db_follow = follow.encode('utf-8')
            db_fans = fans.encode('utf-8')
            statement = "insert into %s value('%s', '%s', '%s', '%s', '%s')" % ('all_sn', db_name, db_area, db_url, db_follow, db_fans)
            cur.execute(statement)
            cur.close()
            self.db.commit()
            for j in info[1][:]:
                [follow, fans, area] = self.all_info(j[1])
                cur = self.db.cursor()
                db_name = j[0].encode('utf-8')
                db_area = area.encode('utf-8')
                db_url = j[1].encode('utf-8')
                db_follow = follow.encode('utf-8')
                db_fans = fans.encode('utf-8')
                statement = "insert into %s value('%s', '%s', '%s', '%s', '%s')" % ('all_sn', db_name, db_area, db_url, db_follow, db_fans)
                cur.execute(statement)
                cur.close()
                self.db.commit()
            # break
            print ''
        '''
          开始进行关系分析
        '''
        # 先输出已经很明晰的关系   sn_relationship
        # for i in all_sn:
            # for j in i[1][:]:
                # print '*************************************************'
                # print j[0], j[1],
                # print u' 关注了 ',
                # print all_sn[0][0], all_sn[0][2]
                # cur = self.db.cursor()
                # from_name = j[0].encode('utf-8')
                # from_url = j[1].encode('utf-8')
                # to_name = all_sn[0][0].encode('utf-8')
                # to_url = all_sn[0][2].encode('utf-8')
                # statement = "insert into %s value('%s', '%s', '%s', %s)" % ('sn_relationship', from_name, from_url, to_name, to_url)
                # cur.execute(statement)
                # cur.close()
                # self.db.commit()

        # 然后再分析各个之间是否存在关注关系   [[name, area, url], [[name, url], [name, url], ...]]
        # print '-----------------------------'
        no_repeat = []
        for i in all_sn:
            # print i
            obj_list = [[i[0][0], i[0][2]]] + i[1][:]     # 取出一个微博信息
            for object in obj_list:
                for j in all_sn:
                    for k in j[1][:]:       # 在每个微博的粉丝信息里面进行查询
                        if object[0] in k[0] or object[1] in k[1]:
                            # print '********************************************'
                            # print object[0], k[0], object[1], k[1]
                            print '********************************************'
                            print object[0], object[1],
                            print u' 关注了 '
                            print j[0][0], j[0][2]
                            cur = self.db.cursor()
                            from_name = object[0].encode('utf-8')
                            from_url = object[1].encode('utf-8')
                            to_name = j[0][0].encode('utf-8')
                            to_url = j[0][2].encode('utf-8')
                            statement = "insert into %s value('%s', '%s', '%s', '%s')" % ('sn_relationship', from_name, from_url, to_name, to_url)
                            cur.execute(statement)
                            cur.close()
                            self.db.commit()
                            break
        # for

    def retrive_fans(self, url, page_num):
        '''
          返回粉丝页面的粉丝信息
        '''
        fan_list = []
        delay = random.uniform(1, 3)
        time.sleep(delay)
        page = self.get_page(url)

        pat = re.compile(u'(?<=<table>).+?(?=</table>)')
        res = pat.findall(page)
        if len(res) == 0:
            return fan_list

        for i in res:
            pat = re.compile(u'(?<=href=").+?(?=">)')
            sub_res = pat.findall(i)
            url = sub_res[0]

            pat = re.compile(u'(?<=">)[^<]+?(?=</a>)')
            sub_res = pat.findall(i)
            name = sub_res[0]

            if u'2671109275' in url:
                continue

            fan_list.append([name, url])

        # 找到下一页的链接
        pat = re.compile(u'(?<=<a href=")[^<]+?(?=">下页</a>)')
        res = pat.findall(page)
        if len(res) == 0:
            return fan_list
        else:
            next_url = u'http://weibo.cn' + res[0]

        next_url = next_url.replace(u'&amp;', u'&')
        page_num = page_num - 1
        if page_num == 0:
            return fan_list
        else:
            return fan_list + (self.retrive_fans(next_url, page_num))

    def get_fans(self, url, depth=0, pagein=None):
        '''
          返回指定深度的粉丝信息
        '''
        if pagein == None:
            page = None
            while page == None:
                delay = random.uniform(1, 3)
                time.sleep(delay)
                page = self.get_page(url)
                if page == False or page == '':
                    print '~~~~~~~~~~~~~~~~~~~~~notice a~~~~~~~~~~~~~~~~~~~~~~~~~'
                    continue
                else:
                    try:
                        # page = page.decode('utf-8')
                        break
                    except:
                        print '~~~~~~~~~~~~~~~~~~~~~notice b~~~~~~~~~~~~~~~~~~~~~~~~~'
        else:
            page = pagein

        # 加入列表，防止以后重复
        self.fans_list.append(url)

        # 打印出自己的名字和url
        pat = re.compile(u'(?<=\<a href=")[^<]+?(?=">资料</a>)')
        res = pat.findall(page)
        info_url = u'http://weibo.cn' + res[0]
        self.url = info_url
        area, tag, intr, name = self.account_info()
        '''
          地区，标签，人物介绍，博客地址
        '''
        print u'Dep: %d/%d' % (depth, self.depth_set),
        print u'姓名：'.encode('gbk') + name.encode('gbk'),
        print u'地区: '.encode('gbk') + area.encode('gbk'),
        print url.encode('gbk')
        if self.db is not None:
            cur = self.db.cursor()
            db_dep = u'%d/%d' % (depth, self.depth_set)
            db_dep = db_dep.encode('utf-8')
            db_name = name.encode('utf-8')
            db_area = area.encode('utf-8')
            db_url = url.encode('utf-8')
            # statement = "insert into %s value(depth varchar(20),name varchar(20), area varchar(20), url varchar(50))" % db_info[5]
            statement = "insert into %s value('%s', '%s', '%s', '%s')" % (self.db_table, db_dep, db_name, db_area, db_url)
            cur.execute(statement)
            cur.close()
            self.db.commit()

            # print name

        if depth == 0:    # 结束了
            print u'end fans-digging!'
            return True

        # 找到下一个粉丝
        pat = re.compile(u'(?<=粉丝\[).+?(?=\])')
        res = pat.findall(page)
        if res[0] == u'0':    # 没有粉丝
            print u'没有粉丝了!'.encode('gbk')
            return True

        pat = re.compile(u'(?<=href=")[^<]+?(?=">粉丝\[)')
        res = pat.findall(page)
        url = u'http://weibo.cn' + res[0]
        url = self.new_fans(url)
        if url == False:
            print u'没有不重复的粉丝了!'.encode('gbk')
            return True

        depth_dec = depth - 1
        delay = random.uniform(1, 3)
        time.sleep(delay)
        # print url, depth_dec
        return self.get_fans(url, depth_dec)

    def new_fans(self, url):
        '''
          找到没有重复过的粉丝，否则结束
        '''
        delay = random.uniform(1, 3)
        time.sleep(delay)
        page = self.get_page(url)
        # page = page.decode('utf-8')

        pat = re.compile(u'(?<=<table>).+?(?=</table>)')
        res = pat.findall(page)
        if len(res) == 0:
            print u'END: 粉丝页没有粉丝了'.encode('gbk'),
            print url
            return False

        for i in res:
            pat = re.compile(u'(?<=href=").+?(?=">)')
            sub_res = pat.findall(i)
            url = sub_res[0]
            if u'2671109275' in url:
                print u'PASS（新手指南）:'.encode('gbk'),
                print url
                continue
            if url not in self.fans_list:
                return url
            else:
                print u'PASS（重复的粉丝）:'.encode('gbk'),
                print url

        # 找到下一页的链接
        pat = re.compile(u'(?<=<a href=").+?(?=">下页</a>)')
        res = pat.findall(page)
        if len(res) == 0:
            print u'END: 没有下一页了'.encode('gbk'),
            print url
            return False
        else:
            next_url = u'http://weibo.cn' + res[0]

        next_url = next_url.replace(u'&amp;', u'&')
        return new_fans(next_url)


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
        [area, tag, intr, name] = self.account_info()

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
        # page = page.decode('utf-8')

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
        pat = re.compile(u'(?<=昵称:).+?(?=<br/>)', re.DOTALL)
        res = pat.findall(page)
        if len(res) == 0:
            name = u''
        else:
            name = res[0].strip(u' ').strip(u'\n')

        return [area, tag, intr, name]


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
        # if str[0]!=u'<' or str[-1]!=u'>':
            # print 'make sure the string is in a HTML format!'
            # return False
            # return str

        while True:
            indexl = str.find(u'<')
            indexr = str.find(u'>')
            if indexl == -1:
                break

            if indexr == -1:
                # print 'make sure the string is in a HTML format!'
                # return False
                return str

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


    def get_page(self, urlin=None):
        '''
          得到指定页面的内容
        '''
        header = self.header
        if urlin == None:
            url = self.url
        else:
            url = urlin
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

        try:
            r = opener.open(req, timeout = 60)
            if r.info().get('Content-Encoding') == 'gzip':
                buf = StringIO.StringIO(r.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read()
            else:
                data = r.read()
        except:
            print 'failed'
            opener.close()
            return False

        try:
            data = data.decode('utf-8')
        except:
            data = self.get_page(url)

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
    # a = u'href="wgfgf.dfdf./dfd?vt=4">'
    # pat = re.compile(u'(?<=href=").+?(?=">)')
    # res = pat.findall(a)
    # print res[0]
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
    a.all_info()
    # a.get_fans(_url, 2)
    # a.account_info()
    # a.get_info()




