
import argparse
import urllib2
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def  get_pdf_url(urllist):
  pdflist = list()
  for url in urllist:
    req = urllib2.Request(
        url = url,
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'}
      )
    content = urllib2.urlopen(req).read()
    bs_page =  BeautifulSoup(content)
    ############### method 2 ##############################
    # pdf = bs_page.find_all('a', {'href': re.compile('.pdf')})
    # for a in pdf:
      # pdflist.append(a.attrs['href'])
      # a.get_text()        # get text
    ################ method use find_all 'a' ##################
    # pdf = bs_page.find_all('a')
    # for a in pdf:
      # if a.attrs['href'][-3:] == 'pdf':
        # pdflist.append(a.attrs['href'])
  # return pdflist

def  read_para_from_xml(fn):
  xml_parse = ET.parse(fn)
  addr =  xml_parse.getroot().findall('addr')
  addrlist = list()
  for s in addr:
    addrlist.append(s.text)
    # print ', '.join(['%s:%s' % item for item in s.__dict__.items()])
    # print s.attrib['id']+'  '+s.text
    # print s.text
  return addrlist



def  main():
  parser = argparse.ArgumentParser(description='gs')
  parser.add_argument('-f', type=str, required=True, metavar='filename', dest='fn', help='Specify the filename')
  args = parser.parse_args().fn
  addr = read_para_from_xml(args);
  print 'url contains PDFs:...'
  for el in addr:
    print '    '+el
  pdfurl = get_pdf_url(addr)
  for el in pdfurl:
    print el


if __name__ == '__main__':
  main()