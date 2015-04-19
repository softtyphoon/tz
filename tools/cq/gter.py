

import urllib
import urllib2
import cookielib
import time
import StringIO
import gzip
import re
import time
import random


def get_content(num, cookie):
      '''
        http://www.gter.net/offer/index/ajax?page=1&page_num=24&kw=
      '''
      header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
          'Host':'www.gter.net',
          'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
          'Connect':'keep-alive',
          'Accept-Encoding':'gzip, deflate'
          }
      if num < 1:
          print u'能设个正确的数么'
          yield False
      else:
          for page in range(1, num+1):
              url = 'http://www.gter.net/offer/index/ajax?page=%d&page_num=24&kw=' % page
              print url
              [page, cookie] = get_page(url_in=url, header_in=header, data=None, cookie_set=cookie)
              yield page


def login(username, password):
    '''
      登陆网站，获得cookie
        打开主页
        请求登陆页面
        请求验证码
        发出登陆请求，获得cookie
    '''
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
              'Host':'www.gter.net',
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
              'Accept-Encoding':'gzip, deflate'
              }
    main_url = u'http://www.gter.net/offer/index'
    login_url = u'http://www.gter.net/index.php?m=user&c=login&api=uicms&infloat=yes&handlekey=login&t=%d&inajax=1&ajaxtarget=fwin_content_login' % (int(time.time()))
    cq_url = u'http://www.gter.net/index/ck.html?width=120&height=30'
    post_url = u'http://www.gter.net/index.php?m=user&c=login&api=uicms&inajax=1&handlekey=lsform'

    # 打开主页，获取cookie
    [page, cookie] = get_page(url_in=main_url, header_in=header, data=None, cookie_set=None)

    # 打开登陆页面
    # image/js/common.js 中
    # showWindow('login', 'index.php?m=user&c=login&api=uicms', 'get',-1);
    # function showWindow(k, url, mode, cache, menuv, cover)
    header['X-Requested-With'] = 'XMLHttpRequest'
    header['Referer'] = main_url
    [page, cookie] = get_page(url_in=login_url, header_in=header, data=None, cookie_set=cookie)
    fn = open('login_page.txt', 'w+')
    fn.write(page)
    fn.close()

    # name="uicms_token" type="hidden" value="2a8e1022"
    page = page.decode('utf-8')
    pat = re.compile(u'(?<=name="uicms_token" type="hidden" value=").+?(?=")', re.DOTALL)
    uicms_token = pat.findall(page)[0]

    # 请求验证码
    del header['X-Requested-With']
    header['Accept'] = 'image/png,image/*;q=0.8,*/*;q=0.5'
    [page, cookie] = get_page(url_in=cq_url, header_in=header, data=None, cookie_set=cookie)
    kkk = open('111111.txt', 'w+')
        
    fn = open('code.png', 'wb+')
    fn.write(page)
    fn.close()

    print u'需要自动识别验证码吗？(Y)否则：请打开 code.png 文件，输入验证码：'
    checkcode = raw_input()
    if checkcode.lower() == 'y':
        for i in cookie:
            if 'checkcode' in i.name:
                checkcode = i.value
        print u'识别出验证码为：%s' % checkcode

    # 提交登陆数据
    # do_submit=1&uicms_token=2a8e1022&from=http%3A%2F%2Fwww.gter.net%2Foffer%2Findex&uiuser=asdasd&uipw=123456&vercode=YLZV
    post_data = {'do_submit':'1',
                 'from':'http://www.gter.net/offer/index',
                 'uicms_token':uicms_token,
                 'uiuser':username,
                 'uipw':password,
                 'vercode':checkcode.lower()
                }
    post_data = urllib.urlencode(post_data)
    kkk.write(post_data)
    kkk.close()
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header['Content-Type'] = 'application/x-www-form-urlencoded'
    header['Connection'] = 'keep-alive'
    [page, cookie] = get_page(url_in=post_url, header_in=header, data=post_data, cookie_set=cookie)
    fn = open('after_post.txt', 'w+')
    fn.write(page)
    fn.close()
    page = page.decode('utf-8')

    if page.find('alert') > -1:
        print u'登陆失败，检查用户名和密码是否错误'
    else:
        print u'登陆成功'
        
    # 还有最后一步跳转
    pat = re.compile(u'(?<=src=").+?(?=")', re.DOTALL)
    reload = pat.findall(page)[0]
    del header['Content-Type']
    header['Host'] = 'bbs.gter.net'
    header['Accept'] = '*/*'
    [page, cookie] = get_page(url_in=reload, header_in=header, data=None, cookie_set=cookie)
    fn = open('ttt.txt', 'w+')
    fn.write(page)
    fn.close()

    return cookie

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
          print 'initial cookie'
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
    # http://www.gter.net/offer/index
    username = 'pp13438845536'        # 用户名和密码
    password = '13438845536'
    page_num = 1                      # 设置页面个数
    # 其他的不用改了
    cookie = login(username, password)
    page_content = get_content(page_num, cookie)
    cnt = 1
    for i in page_content:
        file_name = 'page/page_%d.txt' % cnt
        fn = open(file_name, 'a+')
        fn.write(i)
        fn.close()
        time.sleep(int(random.uniform(1, 2)))
        cnt += 1
    print u'结束！！！'


