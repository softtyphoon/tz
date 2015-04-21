

import urllib
import urllib2
import cookielib
import time
import StringIO
import gzip
import sys
import re
import time
import random
from bs4 import BeautifulSoup

_header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
           'Host':'nba.sports.sina.com.cn',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Connect':'keep-alive',
           'Accept-Encoding':'gzip, deflate'
          }

'''
  赛程相关定义
'''
game_schedule_url = u'http://nba.sports.sina.com.cn/match_result.php?dpc=1'
ranking_url = [u'http://nba.sports.sina.com.cn/league_order1.php?dpc=1', u'http://nba.sports.sina.com.cn/league_order.php?dpc=1']
player_url = u'http://nba.sports.sina.com.cn/playerstats.php?s=0&e=299&key=1&t=1'
sch_info = [u'时间',u'类型',u'客队',u'比分',u'主队',u'客队最高分',u'主队最高分']


def player_info(url = player_url, name = u'威斯布鲁克'):

    page, cookie = get_page(url, _header)
    # with open('test.txt', 'w+') as f:
        # f.write(page)

    page = BeautifulSoup(page)
    main_div = page.find('div', attrs={'id':'table730middle'})
    tr = main_div.find_all('tr')
    title = False
    for i in tr:
        td = i.find_all('td')
        if title == False:
            title = True
            for j in td:
                print j.get_text().strip(),
            print ''
        else:
            if name in td[1].get_text().strip():
                for j in td:
                    print j.get_text().strip(),
                print ''

    pass

def ranking_info(url = ranking_url[1]):
    '''
      得到排名信息
    '''
    page, cookie = get_page(url, _header)
    # with open('test.txt', 'w+') as f:
        # f.write(page)

    page = BeautifulSoup(page)
    main_div = page.find('div', attrs={'id':'table980middle'})
    tr = main_div.find_all('tr')
    for i in tr:
        td = i.find_all('td')
        for j in td:
            print j.get_text().strip(),
        print ''

    pass

def nba_sch_info(url = game_schedule_url):
    '''
      获得 nba 的赛程信息，入口url别改
      BeautifulSoup 会掉信息，避免使用
    '''
    page, cookie = get_page(url, _header)
    # with open('test.txt', 'w+') as f:
        # f.write(page)

    page = page.decode('gbk')
    pat = re.compile(u'(?<=<div align="center">).+?(?=div>)', re.DOTALL)
    div = pat.findall(page)[0]

    pat = re.compile(u'(?<=<tr).+?(?=</tr>)', re.DOTALL)
    trs = pat.findall(div)

    today = True        # 默认当前为今日
    future = False      # 默认当前不是未来赛程

    for i in trs:
        # bgcolor="#FFEFB6"
        pat = re.compile(u'(?<=bgcolor=).+?(?= )', re.DOTALL)
        bgcolor = pat.findall(i)[0].strip()
        bgcolor = bgcolor.replace('"', '').strip()

        # 所有的 td 值
        # pat = re.compile(u'(?<=\>)[^<]+?(?=</td>)', re.DOTALL)
        pat = re.compile(u'<td.+?(?=</td>)', re.DOTALL)
        td = pat.findall(i)
        for (index, val) in enumerate(td):
            td[index] = html_tag_remove(td[index]).strip()

        if bgcolor == '#FFD200':    # title
            date = td[0]
            if not future and not today:
                print u'\n未来赛程'
                future = True

            if today == False:
                print ''
                print date

        if bgcolor == '#FFEFB6':       # info
            if (u'完场' in td[0] or u'赛中' in td[0]) and today is True:
                print u'今日比分'
                print date
                today = False

            print ''
            for (index, value) in enumerate(sch_info):
                print value, ':', td[index]

    return 0

    # page = BeautifulSoup(page)
    # main_div = page.find('div', attrs={'id':'table980middle'})
    # table = main_div.find('table')
    # tr = table.find_all('tr')
    # today = True
    # future = False
    # for i in tr:
        # if i['bgcolor'] == '#FFD200':       # 标题栏
            # date = i.find('td').get_text().strip()
            # if not future and not today:
                # print u'\n未来赛程'
                # future = True

            # if today == False:
                # print ''
                # print date

        # if i['bgcolor'] == '#FFEFB6':       # 信息栏
            # tds = i.find_all('td')
            # if (u'完场' in tds[0].get_text() or u'赛中' in tds[0].get_text()) and today is True:
                # print u'今日比分'
                # print date
                # today = False

            # print ''
            # for (index, value) in enumerate(sch_info):
                # print value, ':', tds[index].get_text().strip()

    # pass

def html_tag_remove(str):
      '''
        通用方法，移除tag
      '''
      pat = re.compile(u'<.+?>', re.DOTALL)
      res = pat.findall(str)
      str_fix = str
      for i in res:
          str_fix = str_fix.replace(i, ' ')
      return str_fix

def get_page(url_in=None, header_in=None, data=None, cookie_set=None):
      '''
        通用方法，请求页面
      '''
      url = url_in
      header = header_in

      opener = urllib2.OpenerDirector()
      http_handler = urllib2.HTTPHandler()
      https_handler = urllib2.HTTPSHandler()

      if cookie_set == None:
          # print 'initial cookie'
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
          r = opener.open(req, timeout = 30)
          # Make sure everything is working ;)
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
          print 'Time out'
          opener.close()
          return False

      return [data, cookie]

if __name__ == "__main__":
    while True:
        print u'请选择命令：'
        print u'  1. 查看联盟排名'
        print u'  2. 查看分区排名'
        print u'  3. 查看比赛信息'
        print u'  4. 查看球员信息'
        print u'  5. 退出'
        cmd = raw_input()
        if cmd == u'5':
            print u'退出程序！ '
            sys.exit(0)

        if cmd == u'1':
            ranking_info(ranking_url[0])

        if cmd == u'2':
            ranking_info(ranking_url[1])

        if cmd == u'3':
            nba_sch_info()

        if cmd == u'4':
            print u'请输入球员姓名:',
            name = raw_input().decode('gbk')
            player_info(url = player_url, name = name)
    pass
