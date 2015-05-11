
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

from patent_query import patent_query

class quey_proc():
    def __init__(self, input_file='setting.csv', output_file=u'结果.csv'):
        self.ifnp = input_file
        self.ifn = ''
        self.ofnp = output_file
        self.sfnpath = 'ea2c86'
        self.sfn= ''

    def del_sf(self):
        if os.path.exists(self.sfnpath):
            os.remove(self.sfnpath)

    def clr_sf(self):
        with open(self.sfnpath, 'w+') as self.sfn:
            self.sfn.write('')

    def get_corp(self):
        bp = []
        if os.path.exists(self.sfnpath):
            self.sfn = open(self.sfnpath, 'r')
            setting = self.sfn.readline().decode('gbk').split(',')
            if len(setting) == 3:
                print u'发现上次爬取断点：', setting[2]
                print u'是否从上次断点处继续爬取？Y是，N从头开始爬取'
                an = raw_input().lower()
                if an == 'y':
                    bp = setting
            self.sfn.close()

        # with open(self.ifnp, 'r') as self.ifn:
            # corps = self.ifn.readline()

        self.ifn = open(self.ifnp, 'r')

        if bp == []:
          st = True
        else:
          st = False

        while True:
            i = self.ifn.readline().strip().decode('gbk').split(',')
            if len(i) < 3:
                break

            if i == bp:
                st = True

            if st:
                self.sfn = open(self.sfnpath, 'w+')
                with open(self.sfnpath, 'w+') as self.sfn:
                    self.sfn.write((u','.join(i)).encode('gbk'))
                yield i

# def test():
    # for i in range(1, 10):
        # time.sleep(5)
        # yield i

if __name__ == "__main__":
    a = quey_proc()
    b = patent_query()
    for i in a.get_corp():
        # print i
        # print u'开始处理：', i[0], i[1], i[2]
        result = b.run(i[2], i[0], i[1])
        b.save2file(result)
        time.sleep(random.uniform(1.5, 2.5))
        a.clr_sf()
    a.del_sf()









