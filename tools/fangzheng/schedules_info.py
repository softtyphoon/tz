

import sys
import re
import urllib
import urllib2
import urlparse
import gzip
import cookielib
import time
import random
import argparse
import MySQLdb
from pytesser import *

class schedules_info():
  def __init__(self, username = '', password = '', db_info = ['localhost', 'root', '123456', 3306, 'weibo']):
      self.db_info = db_info
      self.username = username
      self.password = password
      self.table = {'1':u'星期一',
                    '2':u'星期二',
                    '3':u'星期三',
                    '4':u'星期四',
                    '5':u'星期五',
                    '6':u'星期六',
                    '7':u'星期七'
                   }
      pass

  def run(self):
      info_gen = self.request_form()
      fn = open('all.txt', 'w+')
      cnt = 0
      t = info_gen.next()
      self.init_db(self.db_info, t)
      for i in info_gen:      # [bm, js, sch_info]    sch_info = [day, when, info]
          print '--------------------------------------------------------------'
          fn.write('\n--------------------------------------------------------------\n')
          print u'部门:  %s' % i[0]
          fn.write((u'部门:  %s\n' % i[0]).encode('gbk'))
          print u'教师:  %s' % i[1]
          fn.write((u'教师:  %s\n' % i[1]).encode('gbk'))
          for j in i[3]:
              for k in j:
                  print k
                  fn.write((k).encode('gbk'))
          fn.flush()
          # return 0
      print u'结束了！！！'
      self.conn.close()
      
  def write_db(self, sch_info):
      pass

  def request_form(self):
      '''
        根据当前的状态，得到下次请求的数据
        返回 False 说明数据已经请求完毕
        现在当前学院内轮询每个老师
        完成之后，跳往下一个学院，再一次进行
      '''
      request_url = u'http://jwxt.hyit.edu.cn/(w1wm3bjjb3un42nfftdvww55)/jstjkbcx.aspx?zgh=41230&xm=%CE%A2%C8%ED%BD%B2%CA%A60&gnmkdm=N122303'
      header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
                'Host':'jwxt.hyit.edu.cn',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding':'gzip, deflate',
                'Referer':'http://jwxt.hyit.edu.cn/(w1wm3bjjb3un42nfftdvww55)/jstjkbcx.aspx?zgh=41230&xm=%CE%A2%C8%ED%BD%B2%CA%A60&gnmkdm=N122303',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded'
                }

      # 初次查询的数据
      query_data = dict()
      query_data['__EVENTTARGET'] = 'bm'      # 部门开始
      query_data['__EVENTARGUMENT'] = ''      # 空参数
      query_data['__VIEWSTATE'] = 'dDwzMzg3MTcwNjt0PDtsPGk8MT47PjtsPHQ8O2w8aTwxPjtpPDM+O2k8ND47aTw4PjtpPDE2PjtpPDI2PjtpPDI4PjtpPDMwPjs+O2w8dDx0PHA8cDxsPERhdGFUZXh0RmllbGQ7RGF0YVZhbHVlRmllbGQ7PjtsPHhuO3huOz4+Oz47dDxpPDE2PjtAPDM7MjAxNC0yMDE1OzIwMTMtMjAxNDsyMDEyLTIwMTM7MjAxMS0yMDEyOzIwMTAtMjAxMTsyMDA5LTIwMTA7MjAwOC0yMDA5OzIwMDctMjAwODsyMDA2LTIwMDc7MjAwNS0yMDA2OzIwMDUtMjAwOzIwMDQtMjAwNTsyMDAzLTIwMDQ7MjAwMi0yMDAzO1xlOz47QDwzOzIwMTQtMjAxNTsyMDEzLTIwMTQ7MjAxMi0yMDEzOzIwMTEtMjAxMjsyMDEwLTIwMTE7MjAwOS0yMDEwOzIwMDgtMjAwOTsyMDA3LTIwMDg7MjAwNi0yMDA3OzIwMDUtMjAwNjsyMDA1LTIwMDsyMDA0LTIwMDU7MjAwMy0yMDA0OzIwMDItMjAwMztcZTs+PjtsPGk8MT47Pj47Oz47dDx0PHA8cDxsPERhdGFUZXh0RmllbGQ7RGF0YVZhbHVlRmllbGQ7PjtsPHhxO3hxOz4+Oz47dDxpPDM+O0A8MjsxO1xlOz47QDwyOzE7XGU7Pj47bDxpPDA+Oz4+Ozs+O3Q8dDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+Oz47Oz47Oz47dDx0PHA8cDxsPERhdGFUZXh0RmllbGQ7RGF0YVZhbHVlRmllbGQ7PjtsPGJtO2JtOz4+Oz47dDxpPDIzPjtAPOaVmeWKoeWkhDvmnLrmorDlt6XnqIvlrabpmaI755S15a2Q5LiO55S15rCU5bel56iL5a2m6ZmiO+iuoeeul+acuuW3peeoi+WtpumZojvlu7rnrZHlt6XnqIvlrabpmaI75Lqk6YCa5bel56iL5a2m6ZmiO+eUn+WRveenkeWtpuS4juWMluWtpuW3peeoi+WtpumZojvnu4/mtY7nrqHnkIblrabpmaI75aSW5Zu96K+t5a2m6ZmiO+S6uuaWh+WtpumZojvmsZ/mt67lrabpmaI76K6+6K6h6Im65pyv5a2m6ZmiO+aAneaDs+aUv+ayu+eQhuiuuuivvuaVmeWtpumDqDvmlbDnkIblrabpmaI75L2T6IKy6YOoO+WtpueUn+WkhDvoibrmnK/kuK3lv4M75oub55Sf5bCx5Lia5aSEO+WbvuS5pummhjvnu6fnu63mlZnogrLlrabpmaI75YW25LuWO1xlO1xlOz47QDzmlZnliqHlpIQ75py65qKw5bel56iL5a2m6ZmiO+eUteWtkOS4jueUteawlOW3peeoi+WtpumZojvorqHnrpfmnLrlt6XnqIvlrabpmaI75bu6562R5bel56iL5a2m6ZmiO+S6pOmAmuW3peeoi+WtpumZojvnlJ/lkb3np5HlrabkuI7ljJblrablt6XnqIvlrabpmaI757uP5rWO566h55CG5a2m6ZmiO+WkluWbveivreWtpumZojvkurrmloflrabpmaI75rGf5reu5a2m6ZmiO+iuvuiuoeiJuuacr+WtpumZojvmgJ3mg7PmlL/msrvnkIborrror77mlZnlrabpg6g75pWw55CG5a2m6ZmiO+S9k+iCsumDqDvlrabnlJ/lpIQ76Im65pyv5Lit5b+DO+aLm+eUn+WwseS4muWkhDvlm77kuabppoY757un57ut5pWZ6IKy5a2m6ZmiO+WFtuS7ljtcZTtcZTs+PjtsPGk8MD47Pj47Oz47dDx0PHA8cDxsPERhdGFUZXh0RmllbGQ7RGF0YVZhbHVlRmllbGQ7PjtsPEpTeG07anN6Z2g7Pj47Pjt0PGk8MjY+O0A856iL6Jm5O+W0lOagkea4hTvlsJTpm4U75bCU6ZuFMTvlsJTpm4UxMDvlsJTpm4UxMTvlsJTpm4UxMjvlsJTpm4UxMzvlsJTpm4UxNzvlsJTpm4UxOTvlsJTpm4UyO+WwlOmbhTIwO+WwlOmbhTM75bCU6ZuFNDvlsJTpm4U1O+WwlOmbhTY75bCU6ZuFNzvlsJTpm4U4O+WwlOmbhTk75p2O54ix5Y2OO+i3r+e6ouWGmzvot6/nuqLlhpsv546L6IyC5p6XL+W8oOiOiTvllJDmtIHmlrkv5bqE5YabO+mtj+eEtjvnpZbnu7Q7XGU7PjtAPDYxMDY4OzYxMTMzOzQxMTkwOzQxMTk0OzQxMjAzOzQxMjA0OzQxMjA1OzQxMjA2OzQxMjEwOzQxMjEyOzQxMTk1OzQxMjEzOzQxMTk2OzQxMTk3OzQxMTk4OzQxMTk5OzQxMjAwOzQxMjAxOzQxMjAyOzE1MDk5OzYxMTg4OzYxMTg4OzY2NjY2OzYxMzY4OzYxMjY4O1xlOz4+O2w8aTwwPjs+Pjs7Pjt0PDtsPGk8MT47aTwzPjs+O2w8dDxAMDw7Ozs7Ozs7Ozs7Pjs7Pjt0PEAwPDs7Ozs7Ozs7Ozs+Ozs+Oz4+O3Q8QDA8cDxwPGw8UGFnZUNvdW50O18hSXRlbUNvdW50O18hRGF0YVNvdXJjZUl0ZW1Db3VudDtEYXRhS2V5czs+O2w8aTwxPjtpPDA+O2k8MD47bDw+Oz4+Oz47Ozs7Ozs7Ozs7Pjs7Pjt0PEAwPHA8cDxsPFBhZ2VDb3VudDtfIUl0ZW1Db3VudDtfIURhdGFTb3VyY2VJdGVtQ291bnQ7RGF0YUtleXM7PjtsPGk8MT47aTwyPjtpPDI+O2w8Pjs+Pjs+Ozs7Ozs7Ozs7Oz47bDxpPDA+Oz47bDx0PDtsPGk8MT47aTwyPjs+O2w8dDw7bDxpPDA+O2k8MT47aTwyPjtpPDM+O2k8ND47aTw1PjtpPDY+O2k8Nz47aTw4Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDw2MTA2ODs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85YGc6K++MDI0Mzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8KDIwMTQtMjAxNS0yKS01MjA2NzgwLTYxMDY4LTE7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOWUkOivl+Wui+ivjei1j+aekDs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85ZGoNOesrDnoioLov57nu60y6IqCe+esrDctN+WRqH0vWUZKMDEwMTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8MjAxNS0wNC0xNS0xMS0xODs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85Ye65beuOz4+Oz47Oz47Pj47dDw7bDxpPDA+O2k8MT47aTwyPjtpPDM+O2k8ND47aTw1PjtpPDY+O2k8Nz47aTw4Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDw2MTA2ODs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85YGc6K++MDI0NDs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8KDIwMTQtMjAxNS0yKS01MjA2NzgwLTYxMDY4LTE7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOWUkOivl+Wui+ivjei1j+aekDs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85ZGoNeesrDfoioLov57nu60y6IqCe+esrDctN+WRqH0vWUZKMDEwMzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8MjAxNS0wNC0xNS0xMS0xODs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85Lya6K6uOz4+Oz47Oz47Pj47Pj47Pj47Pj47Pj47Pv0/BTeEGO9RPu9rHAm5z0vdwrka'                    # 状态参数
      query_data['bm'] = '教务处'                          # 部门从空参数开始
      query_data['__VIEWSTATEGENERATOR'] = 'E6032F7F'      # 查询生成器
      query_data['xn'] = '2014-2015'      # 学年
      query_data['xq'] = '2'              # 学期
      query_data['TextBox1'] = ''         # 空的
      query_data['js'] = '12345'         # 教师编号，开始随便填

      post_data = urllib.urlencode(query_data)
      end = False

      # 先打开一次，获得所有的部门编码
      page = False
      while page == False:
          delay = random.uniform(1,2)
          # time.sleep(delay)
          page = self.get_page(request_url, header, post_data)
      # fn = open('info_page.txt', 'r')
      # page = fn.read()
      # fn.close()
      page = page.decode('gb2312')
      pat = re.compile(u'(?<=<select name="bm").+?(?=</select>)', re.DOTALL)
      res = pat.findall(page)
      pat = re.compile(u'(?<=>).+?(?=</option>)')
      all_bm = pat.findall(res[0])
      yield all_bm            # 第一次返回全部部门，用来建立数据库的表
      # for i in all_bm:
          # print i

      for bm in all_bm:
          print 'test p'
          # if u'经济管理学院' not in bm:     # 测试
              # print 'pass', bm, 'a'
              # continue
          # 再对当前部门发出一次请求，获得所有的老师编号
          query_data['bm'] = bm.encode('gbk')
          query_data['__EVENTTARGET'] = 'bm'
          post_data = urllib.urlencode(query_data)
          if bm is not all_bm[0]:
              # print 'oooook1'
              page = False
              while page == False:
                  delay = random.uniform(1,2)
                  # time.sleep(delay)
                  page = self.get_page(request_url, header, post_data)
              try:
                page = page.decode('gb2312')
              except:
                  try:
                      page = page.decode('gbk')
                  except:
                      page = page
                      
              
          # 获得 __VIEWSTATE ，不然会查询失败
          # name="__VIEWSTATE" value="
          pat = re.compile(u'(?<=name="__VIEWSTATE" value=").+?(?=")', re.DOTALL)
          res = pat.findall(page)
          query_data['__VIEWSTATE'] = res[0]

          # 获得当前部门所有老师的编号
          pat = re.compile(u'(?<=<select name="js").+?(?=</select>)', re.DOTALL)
          res = pat.findall(page)
          # pat = re.compile(u'(?<=>).+?(?=</option>)')
          pat = re.compile(u'(?<=value=")\d+?(?=">)')
          all_js = pat.findall(res[0])
          pat = re.compile(u'(?<=>).+?(?=</option>)')
          all_js_name = pat.findall(res[0])

          # 针对每位教师
          for (js_num, js) in enumerate(all_js):
              # print '--------------------------------------------------------------'
              # print u'部门:%s' % bm
              # print u'教师:%s' % all_js_name[js_num]
              query_data['js'] = js
              query_data['__EVENTTARGET'] = 'js'
              post_data = urllib.urlencode(query_data)
              if js is not all_js[0]:
                  # print 'oooook2'
                  page = False
                  while page == False:
                      delay = random.uniform(1,2)
                      # time.sleep(delay)
                      page = self.get_page(request_url, header, post_data)
                  temp = (u'del\\'+all_js_name[js_num]+u'.txt').replace(u'/', '')
                  f = open(temp, 'w+')
                  f.write(page)
                  f.write(post_data)
                  f.close()
                  try:
                    page = page.decode('gb2312')
                  except:
                      try:
                          page = page.decode('gbk')
                      except:
                          page = page
              # 用于测试
              # f = open('info_page.txt', 'r')
              # page = f.read()
              # f.close()
              # page = page.decode('gb2312')
              # 提取课表信息
              pat = re.compile(u'(?<=<table id="Table6").+?(?=</table>)', re.DOTALL)
              table = pat.findall(page)[0]

              pat = re.compile(u'(?<=<tr>).+?(?=</tr>)', re.DOTALL)
              trs = pat.findall(table)

              sch_info = []
              available = [1, 1, 1, 1, 1, 1, 1]     # 七天
              # 针对七天的每个时段，每节课进行循环
              # 通过分析课表得到：连续两节课的必从单数课开始
              for i in range(2, len(trs)):    # 从第2个开始，前面两个分别是 日期栏 和 早晨
                  if i % 2 == 0:
                      available = [1, 1, 1, 1, 1, 1, 1]
                  tr = trs[i]
                  # 划出实际课表信息的内容
                  td = tr[tr.find(u'<td align="Center"'):]

                  # 找到具体的课程信息
                  # pat = re.compile(u'(?<=>)[^(td)]+?(?=</td>)', re.DOTALL)
                  pat = re.compile(u'<td.+?</td>', re.DOTALL)
                  lesson = pat.findall(td)      # 当前时间段一周内安排的课程信息
                  all_l = list()
                  # day_code = range(7)
                  # 对当前课程的有效日期进行提取
                  day_code = []
                  for (num, avai) in enumerate(available):
                          if avai == 1:
                              day_code.append(num)
                  for (num, j) in enumerate(lesson):
                      pat = re.compile(u'(?<=>).+?(?=</td>)', re.DOTALL)
                      res = pat.findall(j)
                      if res[0] == '&nbsp;':
                          day_code.pop(0)
                          continue
                      day_code.append(day_code.pop(0))
                  # print lesson
                  # 当前时间段一周内安排的课程信息
                  for (num, j) in enumerate(lesson):
                      pat = re.compile(u'(?<=>).+?(?=</td>)', re.DOTALL)
                      res = pat.findall(j)
                      if res[0] == '&nbsp;':
                          continue
                      pat = re.compile(u'(?<=rowspan=")\d+?(?=")', re.DOTALL)
                      rawspan = pat.findall(j)                                      # 所有有效课的 rawspan
                      all_l.append(self.html_tag_remove(res[0]))                    # 有效课的信息
                      # print 'rawspan:', rawspan
                      # print available

                      # 根据得到的课程信息，生成表达课程表安排的字符串
                      for (num, avai) in enumerate(available):
                          if avai == 1:
                              if rawspan == []:
                                  span = '1'
                              else:
                                  span = rawspan.pop(0)
                              if str(span) == '1':
                                  when = u'第%d节' % (i-1)
                              else:
                                  when = u'第%d/%d节' % (i-1, i)
                                  available[num] = 0

                              day = self.table[str(day_code.pop(0)+1)]
                              info = all_l.pop(0)
                              sch_info.append([day, when, info])
                              # print '==========================================='
                              # print day, when, info
                              break

              yield [bm, all_js_name[js_num], js, sch_info]

                  # for k in all_l:
                      # print k

                      # print self.html_tag_remove(i)
                  # print td
                  # for i in td:
                      # print i
                  # yield page


  def html_tag_remove(self, str):
      pat = re.compile(u'<.+?>', re.DOTALL)
      res = pat.findall(str)
      str_fix = str
      for i in res:
          str_fix = str_fix.replace(i, ' ')
      return str_fix

  def login(self):
      '''
        登陆
        主页地址
          http://jwxt.hyit.edu.cn/%28w1wm3bjjb3un42nfftdvww55%29/default2.aspx
      '''
      header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
                'Host':'jwxt.hyit.edu.cn',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive'
                }

      login_url = u'http://jwxt.hyit.edu.cn/%28w1wm3bjjb3un42nfftdvww55%29/default2.aspx'
      host = urlparse.urlparse(login_url).netloc

      # 打开主页
      login_page = self.get_page(login_url, header)
      # fn = open('login_page.txt', 'r+')
      # login_page = fn.read()
      # fn.close()

      # 构造登陆数据
      post_data = dict()

      pat = re.compile(u'(?<=name="__VIEWSTATE" value=").+?(?=")', re.DOTALL)
      res = pat.search(login_page)
      post_data['__VIEWSTATE'] = res.group()

      pat = re.compile(u'(?<=name="__VIEWSTATEGENERATOR" value=").+?(?=")', re.DOTALL)
      res = pat.search(login_page)
      post_data['__VIEWSTATEGENERATOR'] = res.group()

      post_data['TextBox1'] = self.username
      post_data['TextBox2'] = self.password

      post_data['RadioButtonList1'] = u'教师'.encode('gbk')
      post_data['Button1'] = u''
      post_data['lbLanguage'] = u''

      # 下载验证码
      header['Accept'] = 'image/png,image/*;q=0.8,*/*;q=0.5'
      header['Referer'] = login_url
      img_url = u'http://jwxt.hyit.edu.cn/%28w1wm3bjjb3un42nfftdvww55%29/CheckCode.aspx'
      img = self.get_page(img_url, header)
      fn = open('code.gif', 'wb+')
      fn.write(img)
      fn.close()

      print u'请打开 code.gif 文件，输入验证码：'
      checkcode = raw_input()
      post_data['TextBox3'] = checkcode.lower()

      str = urllib.urlencode(post_data)

      # 进行验证
      header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      login_page = self.get_page(login_url, header, str)
      # fn=open('after_login.txt', 'w+')
      # fn.write(login_page)
      # fn.close()

      login_ok = u'<title>Object moved</title>'
      if login_ok in login_page:
          print u'登陆成功!'
          return True
      else:
          print u'登陆失败'
          return False

  def get_page(self, url_in=None, header_in=None, data=None):
      '''
        通用方法，请求页面
      '''
      if url_in is None:
          url = self.url
      else:
          url = url_in

      if header_in is None:
          header = self.header
      else:
          header = header_in

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
          opener.close()
          return False
      # try:
          # data = data.decode('utf-8')
      # except:
          # data = self.get_page(url)

      return data
      
  def init_db(self, db_info, table_info):
      '''
        初始化数据库    db_set = ['localhost', 'root', '123456', 3306, 'weibo']
      '''
      existed =[False, False]
      con = MySQLdb.connect(host=db_info[0], user=db_info[1], passwd=db_info[2], port=db_info[3], charset='utf8')
      statement = "show databases"
      cursor = con.cursor()
      cursor.execute(statement)
      result = cursor.fetchall()
      for i in result:
          if db_info[4] in i:
              existed[0] = True
              break

      if existed[0] is True:
          print u'INFO: 设置的数据库已经存在，是否删除(Y)重建'.encode('gbk')
          sel = raw_input()
          if sel.lower() == u'y':
              statement = "drop database %s" % db_info[4]
              cursor.execute(statement)
              statement = "create database %s" % db_info[4]
              cursor.execute(statement)
              print 'OK: create database %s' % db_info[4]
      else:
          statement = "create database %s" % db_info[4]
          cursor.execute(statement)
          print 'OK: create database %s' % db_info[4]

      con.select_db(db_info[4])
      print 'OK: selected database %s' % db_info[4]
      
      for t in table_info:
          statement = "create table %s(name varchar(20), kebiao varchar(5000))" % t
          cursor.execute(statement)
          print 'OK: create table(%s) cause the table is not exist in database %s' % (t, db_info[4])

      cursor.close()
      self.conn = con


if __name__ == "__main__":
    # a = {'a':'教务处'}
    # print urllib.urlencode(a)
    # im = Image.open('ck.png')
    # text = image_to_string(im)
    # print text
    # text = image_file_to_string('ck.png', graceful_errors=True)
    # print "Using image_file_to_string():"
    # print text
    # sys.exit(0)
    b = '<f>fsd<sfdf>dser<f.f>'
    a = schedules_info('41230', 'hyitJSJ11416')
    # a.html_tag_remove(b)
    # a.login()
    a.run()
    


























