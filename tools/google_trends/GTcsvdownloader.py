

import urllib2
import gzip
import csv
import sys
import random
import time
from StringIO import StringIO


class GTcsvdownloader():
  '''
  downloader csv file from www.google.com/trends
  '''

  def __init__(self, key_word):
    self.header = {
        u'Host':u'www.google.com',
        u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
        u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        u'Accept-Encoding':u'gzip, deflate',
        u'Referer':u'http://www.google.com/trends/explore',
        u'Cookie':u'__utma=173272373.973540543.1426308837.1426308837.1426308837.1; __utmb=173272373.19.10.1426308837; __utmc=173272373; __utmz=173272373.1426308837.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_~1=1; __utmt_~2=1; I4SUserLocale=zh_CN; __utma=173272373.973540543.1426308837.1426308837.1426308837.1; __utmb=173272373.20.9.1426309376527; __utmc=173272373; __utmz=173272373.1426308837.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; NID=67=kForb6sR8_qAJz568PcBGsvl5Dq-hvldhywOjBT_iW6pCAeFwJ55otw0QzRewW9We1nC2MAPFtJpO4ZwMDRp1XGtB1GloKr7CgUSVRg_uzHZICy8lwlbn8RgU-pVQk8WAxbfhugn; S=izeitgeist-ad-metrics=U1cwTXnqTFs; OGP=-4061129:; PREF=ID=b1b45a10f51dc59b:FF=0:TM=1426309029:LM=1426309029:S=JqF1FtAlcveQxszj; SID=DQAAANAAAAAp0BjgED18DL-hAiw9FB7ZBpttsqJmjz-Sjc3NDJ46OFsQMLZ2wbh4DOA6eoZhJCm2yVYbNW5yHZdxV8pxPtaHJvWaI-HkAtSnB-7qz1ayufpL-V2wteBQFRDqBgQnd1nq0JnQG6Jl_xSrwnU5WZYvrAmk7fMKBW9WBSnZ_U4NYQ5HTjw0mBlYj3du5Sn2TnuMpIKbBAgWiS4PtOIK7DTPWYrHr9NAx0c4dbt3Qlem-dsKkN33WhmIaoOeng7Cx6HNOhpN0s3XNkcTmfdE1lxy; HSID=AR7KY08SMWom3T6rm; APISID=Zwh7tBCYOWBDYBWY/ALhWoN0608IvwOK3N',
        u'Connection':u'keep-alive'
      }
    self.name = key_word
    self.timeout = 60
    self.url = u'http://www.google.com/trends/trendsReport?hl=zh-CN&q='+key_word+u'&geo=GB&cmpt=q&tz&tz&content=1&export=1'

  def get_csv(self):
    '''
    messy code solution: b.decode('utf-8').encode('gbk')
    '''
    opener = urllib2.OpenerDirector()
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(self.url)
    for (name, val) in self.header.items():
      req.add_header(name, val)

    try:
      r = opener.open(req, timeout = self.timeout)
    except:
      print 'failed'
      opener.close()
      r.close()
      sys.exit(0)
    # Make sure everything is working ;)
    if not r.info().has_key('Content-Disposition'):
      print "You've exceeded your quota. Continue tomorrow..."
      opener.close()
      r.close()
      sys.exit(0)

    if r.info().get('Content-Encoding') == 'gzip':
      buf = StringIO(r.read())
      f = gzip.GzipFile(fileobj=buf)
      data = f.read()
    else:
      data = r.read()

    myFile = open(u'%s_trends.csv' % (self.name), 'w+')
    print u'writing to file %s_trends.csv...' % (self.name),
    myFile.write(data)
    myFile.close()
    print u'done!'
    opener.close()
    r.close()

if __name__ == '__main__':
  a = open(u'csv_file/AAL_trends.csv', 'r')
  c = open(u'csv_file/recode/AAL_trends.csv', 'w+')
  for b in a.readlines():
    print b
    d = b.decode('utf-8').encode('gbk')
    print d
    c.write(d)
  a.close()
  c.close()
  sys.exit(0)
  a = GTcsvdownloader(u'durrant')
  a.get_csv()
  sys.exit(0)
  # read file
  file_name = [u'G1.txt', u'G2.txt']
  count = 1
  for f in file_name:
    fn = open(f)
    for code in fn.readlines():
      code = code.strip('\n')
      a = GTcsvdownloader(code)
      a.get_csv()
      delay = random.uniform(10, 40)
      delay = int(delay)
      time.sleep(delay)



