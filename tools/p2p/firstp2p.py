#codng:utf-8
from bs4 import BeautifulSoup


type = {
    'crd':u'产融贷',         # icon_melting
    'ysd':u'应收贷',         # icon_ysd'
    'a':u'd'
}


def get_primary_table():
    return 0



def get_sub_table():
    return 0








if __name__ == "__main__":
    fn = open('a.txt', 'r+')
    c = fn.read()
    bs = BeautifulSoup(c)
    b = bs.find_all('div', attrs={'id':'index_list_tab'})
    d = b[0].find_all('div', attrs={'class':'tc'})
    for a in d:
      print a.contents[0]
    # print repr(d)






























