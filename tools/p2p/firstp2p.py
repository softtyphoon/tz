#codng:utf-8
from bs4 import BeautifulSoup
# from task_exec import task_exec
from fund_info import fund_info
import sys
import urllib2
import re
import gzip
import types
import random
import time
import copy




main_url = u'http://www.firstp2p.com/'
_header = {
    u'Host':u'www.firstp2p.com',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Referer':u'http://www.firstp2p.com/',
    # u'Cookie':u'PHPSESSID=emk4jof8co8osccrrfao3vu0b0; _ncfdm=; _ncftr=; _ncf1=1427351222717.6764.0003.0002.0003.0002.0; _ncf2=1427351222717.8047.0003.0002; _ncf3=1427351254278.3.31561.6574.1.61744; mlta=%7B%22mltn%22%3A%7B%22250582%22%3A%5B%226729839450975941527%3E2%3E1427351254237%3E1%3E1427351254180%3E6729839450949563443%3E1427351228421%22%2C1442903254393%5D%7D%2C%22mlti%22%3A%7B%22250582%22%3A%5B%22142735122633671481%22%2C1442903226336%5D%7D%2C%22mltmapping%22%3A%7B%220%22%3A%5B1%2C1429943254395%5D%7D%2C%22mlts%22%3A%7B%22250582%22%3A%5B%225%22%2C1442903254334%5D%7D%7D; fpid=449038',
    u'Connection':u'keep-alive'
}

class firstp2p():

    def __init__(self, url=None, header=None, data=None):
        self.set_param(url, header, data)
        # self.last = [0, 0, 0, 0, 0, 0, [0, 0, 0, 0]]         # 依次为：项目地址，投资总额，可投金额，剩余时间，可投金额差值，可投金额差值是否比上次的大(1)，年化收益率
        self.last = None         # 依次为：项目地址，投资总额，可投金额，剩余时间，可投金额差值，可投金额差值是否比上次的大(1)，年化收益率
        self.delay_level = 0                # 爬取间隔等级，0=[5-15], 1=[15-25], 2=[25, 35], 3=[35, 45], 4=[45, 55], 5=[55, 65]...
        self.delay_max_level = 100          # 爬取的间隔等级最大值
        self.level_up = 0                   # 0.步长不变，1.步长增加，2.步长减少
        self.f_header = header

    def set_param(self, url=None, header=None, data=None):
        self.url = url
        self.header = header
        self.data = data

    def get_page(self):
        opener = urllib2.OpenerDirector()
        http_handler = urllib2.HTTPHandler()
        https_handler = urllib2.HTTPSHandler()
        opener.add_handler(http_handler)
        opener.add_handler(https_handler)
        req = urllib2.Request(self.url)
        for (name, val) in self.header.items():
            req.add_header(name, val)
        if self.data is not None:
            req.add_data(self.data)

        while True:
            try:
                r = opener.open(req, timeout = 60)
                break
            except:
                time.sleep(5)
                continue
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

        opener.close()
        return data

    def get_status(self, content=None):
        '''
          解析主页，得到各个项目的信息
          返回列表数据，依次为：项目地址，投资总额，可投金额，剩余时间，可投金额差值，可投金额差值是否比上次的大(1)，[年化收益率，期限，收益方式，优惠]
        '''
        funds = list()
        if content is None:
            page = self.get_page()
        else:
            page = content

        bs = BeautifulSoup(page)
        fund_url = list()
        tbody = bs.find_all('tbody', attrs={'class':'j_index_tbody'})
        trs = tbody[0].find_all('tr')
        for tr in trs:
            sub = list(range(7))
            atag =  tr.find('a')
            if atag is None:
                continue
            sub[0] = (atag['href'])                  # 获得项目地址
            # print atag['href']

            atag =  tr.find_all('div', attrs={'class':'pro_links'})
            str = atag[0].get_text()
            c = repr(str)
            pat = re.compile(r'(?<=1a).*(?=\\u4e07)')
            b = pat.findall(c)
            sub[1] = (int(float(b[0])*10000))        # 获得项目资金
            # print b[0]


            atag =  tr.find_all('div', attrs={'class':'pl20'})
            text = atag[0].get_text().strip('\n')
            a = atag[0].get_text().strip('\n')
            text = repr(text)
            pat = re.compile(r'(?<=ff1a).*(?=\\u5143)')
            st = pat.findall(text)
            st = st[0].replace(',', '')
            sub[2] = (int(float(st)))                # 获得已投金额
            # print atag[0].get_text().strip('\n')

            day = 0
            hour = 0
            min = 0
            pat = re.compile(u'(?<=：).*(?=天)')
            try:
                day = pat.search(a).group()
            except:
                day = 0

            pat = re.compile(u'(?<=天).*(?=时)')
            try:
                hour = pat.search(a).group()
            except:
                pat = re.compile(u'(?<=：).*(?=时)')
                try:
                    hour = pat.search(a).group()
                except:
                    hour = 0

            pat = re.compile(u'(?<=时)\d*(?=分)')
            try:
                min = pat.search(a).group()
            except:
                pat = re.compile(u'(?<=：)\d*(?=分)')
                try:
                    min = pat.search(a).group()
                except:
                    min = 0
            # print day, hour, min

            time_left = int(day)*24*60 + int(hour)*60 + int(min)      # 获得项目剩余时间，分钟为单位
            # print time_left
            sub[3] = (time_left)

            # 添加，年化收益率      "btm f14 tc">8.50<em>%</em>
            subb = list(range(5))
            pat = re.compile(u'(?<=btm f14 tc">).*(?=<em>%</em>)')
            atag =  tr.find_all('p', attrs={'class':'btm f14 tc'})
            subb[0] = atag[0].get_text().strip('\n')
            subb[1] = atag[1].get_text().strip('\n')
            subb[1] = subb[1].strip(' ')
            atag =  tr.find_all('p', attrs={'class':'date tc'})              #<p class="date tc">按月付息到期还本</p>
            subb[2] = atag[0].get_text().strip('\n')
            atag =  tr.find_all('span', attrs={'class':'icon_new j_tips'})
            if len(atag) == 0:
                subb[3] = 0
                subb[4] = u''
            else:
                subb[3] = 1
                subb[4] = atag[0].get_text()
            sub[6] = subb
            # print subb[4]
            funds.append(sub)

        # if self.last[0] == 0:       # self.last 并没有有效数据
            # self.last = funds
        for (i, j) in  enumerate(funds):
            if self.last is None:
                j[4] = 0
                j[5] = 0
            else:
                j[4] = self.last[i][2] - j[2]
                
                if j[4] > self.last[i][4]:
                    j[5] = 1           # 差值变大，说明买的人增多
                else:
                    j[5] = 0           # 差值变小，说明买的人减少
            funds[i] = j
        return funds

    def decision_maker(self, funds=None):
        '''
          根据项目状态，决定是否进行数据爬取
          传入参数funds，为函数get_status()的返回值，列表数据，依次为：
              项目地址，投资总额，可投金额，剩余时间，可投金额差值，可投金额差值是否比上次的大(1)，[年化收益率，期限，收益方式，优惠]
          判断策略：
            1. 剩余可投金额：少于总额的20%；两次减少的间隔超过了总金额的10%
            2. 剩余时间：少于30分钟
        '''
        # return True     # 用于测试
        # 找到对应的上次的funds信息
        id = funds[0]
        # print '------------------'
        print id
        if self.last is None:
            print 'first time'
            return True
        funds_last = None
        for i in self.last:
            # print i
            index = i.count(id)
            print index
            if index > 0:
                funds_last = i
                break
        if funds_last is None:
            print 'new item'
            return True         # 新加入的项目
        # 先进行下次采样步长的判定，降低步长有最大优先级
        thr = funds[1]*0.01
        if self.level_up != 2:      # 尚未被设置为减少步长
            if funds[4] > (funds[1]*0.1):   #这次采样期间，已经被买走了超过10%
                self.level_up = 2
            elif (funds[5] == 1) and (funds_last[5] == 1):   # 连续两次间隔期间，减少的投资额成增加趋势，买的人越来越多
                self.level_up = 2
            elif (funds[5] == 0) and (funds_last[5] == 0):   # 连续两次间隔期间，减少的投资额成减少趋势，买的人越来越少
                self.level_up = 1
            elif (funds[4] <thr) and (funds_last[4] <thr):   # 连续两次，买的金额都少于总额的1/100
                self.level_up = 1
            else:
                self.level_up = 0


        # 本项目是否需要采样的判定
        if funds is None or len(funds) == 0:
            return False

        part = float(funds[2])/funds[1]
        if part < 0.2:
            print 'total limit'
            return True

        if funds[3] < 30:
            print 'time limit'
            return True

        # print self.last
        if funds_last[2] != 0:
            sub = funds_last[2] - funds[2]
            part = float(sub)/funds[1]
            if part >= 0.1:
                print 'change limit'
                return True
        return False

    def run(self):
        '''
          主函数
          20150329：撤出了多进程方法
        '''
        # 首先，得到所有可投项目的信息
        funds = self.get_status(None)
        # 启动进程
        # tasks = multiprocessing.JoinableQueue()
        # results = multiprocessing.Queue()
        # num_proc = 3        # 启动三个进程
        # procs = [ task_exec(tasks, results)
                  # for i in range(num_proc) ]
        # for p in procs:
            # p.start()
        # 主循环
        pri_table = open('csv/main.csv', 'a+')
        last_p = list()
        times = 0
        while True:
            cur_p = list()
            num_jobs = 0
            for f in funds:       # 逐个进行判定
            #返回列表数据，依次为：项目地址，投资总额，可投金额，剩余时间，可投金额差值，可投金额差值是否比上次的大(1)，[年化收益率，期限，收益方式，优惠]
                go = self.decision_maker(f)
                # go = True     # 由于测试
                if go:
                    # 启动一个进程，进行该项目的爬取
                    print 'go to: %s' % f[0]
                    fund_done = False
                    while fund_done is False:     # 一直尝试，直到完成为止
                        task = fund_info(url=f[0], header=self.f_header, data=None, page = None, funds=f)
                        # [no, type, name, no2, total, profit, date, bonus, bonus_name]
                        result = task.run()
                        if result is False:
                            # 重新登陆，获取新cookie
                            print 'relogin . . .'
                            time.sleep(3)
                            continue
                        else:
                            print 'success: %s' % (f[0])
                            # for i in result:
                                # print i
                            cur_p.append(result[0])
                            if last_p.count(result[0]) == 0:
                                # pri = ','.join(result)
                                id = result[0]
                                if self.last is None:
                                    for i in result:
                                         pri = i+ ','
                                         pri_table.writelines(pri)
                                    pri_table.writelines('\n')
                                    pri_table.flush()
                                else:
                                    for i in self.last:
                                      index = i.count(id)
                                      if index == 0:
                                          for i in result:
                                              pri = i+ ','
                                              pri_table.writelines(pri)
                                          pri_table.writelines('\n')
                                          pri_table.flush()
                                          break
                            fund_done = True
                else:
                    print 'Pass: %s' % (f[0])
            # 等待所有任务完成
            # 爬取间隔控制
            if self.level_up == 2:      # 步长减少
                if self.delay_level > 20:
                    self.delay_level = self.delay_level - 10
                else:
                    self.delay_level = self.delay_level - 1
            elif self.level_up == 1:    # 步长增加
                if self.delay_level > 10:
                    self.delay_level = self.delay_level + 10
                else:
                    self.delay_level = self.delay_level + 1

            if self.delay_level > self.delay_max_level:
                self.delay_level = self.delay_max_level
            elif self.delay_level < 0:
                self.delay_level = 0

            delay_time = self.delay_level*10+5
            # delay_sec = random.uniform(delay_time, delay_time + 10)
            delay_sec = random.uniform(10, 15)
            print 'waiting ... ... ... %d second' % delay_sec
            time.sleep(int(delay_sec))
            self.last = copy.copy(funds)
            funds = self.get_status(None)
            times += 1
            if times == 4:
                sys.exit(0)

        print 'done, never reach here'



if __name__ == "__main__":
    while True:
        try:
            a = firstp2p(main_url, _header)
            a.run()

            if is_sigint_up:
                print "Exit"
                break
        except KeyboardInterrupt:
            print 'exit'
            sys.exit(0)
        # except:
            # a = None
    sys.exit(0)
# total: tbody, j_index_tbody
# 可投金额：<em class="color-yellow1">737,682.86元</em>
# 总额：<div class="pro_links">
                                # 总额：100.00万
                                                                # <i class="badge"
      # atag =  a.find_all('div', attrs={'class':'pro_links'})
      # str = atag[0].get_text()
      # c = repr(str)
      # pat = re.compile(r'(?<=1a).*(?=\\u4e07)')
      # b = pat.findall(c)
      # print b[0]
# 剩余时间：<p>可投金额：<em class="color-yellow1">997,412.84元</em></p>
                            # <p>剩余时间：6天23时57分</p>

























