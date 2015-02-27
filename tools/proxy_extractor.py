

from bs4 import BeautifulSoup
import urllib2


# example addr: http://proxy.com.ru/list_1.html
def  get_proxy_list(url, num):
  proxy_list = list()
  opener = urllib2.OpenerDirector()
  handler = urllib2.HTTPHandler()
  opener.add_handler(handler)
  req = urllib2.Request(url)
  response = opener.open(req)
  content = response.read()
  bs = BeautifulSoup(content)
  # print bs
  tag_b = bs.find_all('b')
  st = False
  cnt = 0
  for a in tag_b:
    ip_indexa = a.next_sibling
    if ip_indexa is not None and ip_indexa.string == str(num*50-50+1):
      st = True
    if st == True:
      ip_index = ip_indexa.next_sibling
      ip = ip_index.next_sibling
      # print ip_index.string, ip.string
      proxy = {'ip':ip_index.string,
               'port':ip.string}
      proxy_list.append(proxy)
      cnt = cnt + 1
    if cnt == 50:
      return proxy_list

def main():
  proxy_list = get_proxy_list('http://proxy.com.ru/list_2.html', 2)
  print proxy_list

if __name__ == '__main__':
  main()
