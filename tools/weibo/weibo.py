



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
from WBlogin import WBlogin
from WBinfo import WBinfo
import MySQLdb
# from bs4 import BeautifulSoup


_header_for_info = {
    u'Host':u'weibo.cn',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Connection':u'keep-alive'
    }

_header_for_login = {
    # u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Content-Type':u'application/x-www-form-urlencoded',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Referer':u'http://www.weibo.cn',
    u'Host':u'login.weibo.cn',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Connection':u'Keep-Alive'
    }

_header_a = {
    u'Host':u'newlogin.sina.cn',
    u'User-Agent':u'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    u'Accept-Language':u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    u'Accept-Encoding':u'gzip, deflate',
    u'Referer':u'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=',
    u'Connection':u'keep-alive'
    }

def init_db(db_info):
    '''
      初始化数据库
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

    if existed[0] is False:
        statement = "create database %s" % db_info[4]
        cursor.execute(statement)
        print 'OK: create database %s' % db_info[4]
    else:
        con.select_db(db_info[4])
        print 'OK: selected database %s' % db_info[4]

    statement = "show tables"
    cursor.execute(statement)
    result = cursor.fetchall()
    for i in result:
        if db_info[5] in i:
            existed[1] = True
            break

    if existed[1] == True:
        print u'INFO: 设置的表已经存在，是否删除(Y)重建，否则程序将退出'.encode('gbk')
        sel = raw_input()
        if sel.lower() == u'y':
            statement = "drop table %s" % db_info[5]
            cursor.execute(statement)
            print 'ATTENTION: table(%s) exists in databases, drop it to create a new one' % db_info[5]
        else:
            cursor.close()
            con.close()
            print u'ATTENTION: 表名称重复，请重新设置表名后再执行程序.'.encode('gbk')
            sys.exit(0)

    statement = "create table %s(depth varchar(20),name varchar(200), area varchar(200), url varchar(500))" % db_info[5]
    cursor.execute(statement)
    print 'OK: create table(%s) cause the table is not exist in database %s' % (db_info[5], db_info[4])
    # else:
        # print 'OK: table(%s) exist in database %s' % (db_info[5], db_info[4])

    # a = u'好'.encode('utf-8')
    # statement = "insert into test value('%s', 'a', 'a', 'a')" % a
    # cursor.execute(statement)
    # con.commit()
    
    cursor.close()
    return con
    # con.close()



if __name__ == "__main__":
    # _url = 'http://weibo.cn/lqszjx'# ?vt=4'
    # 设置起始微博的网址
    _url = 'http://weibo.cn/2053134003'# ?vt=4'
    # 设置用户名
    username = '18817391791'
    # 设置密码
    pwd = 'Sz3205031993'
    # 设置深度
    depth = 100
    # 数据设置，依次为：主机地址，用户名，密码，端口号，数据库名称，表名称
    db_set = ['localhost', 'root', '123456', 3306, 'weibo', 'test']
    db_con = init_db(db_set)
    # sys.exit(0)
    _url_login = u'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
    a = WBlogin(_url_login, _header_for_login, None, username, pwd, _header_a)
    cookie_list = a.login()
    a = WBinfo(_url, _header_for_info, cookie_list, depth, [db_con, db_set[5]])
    a.get_fans(_url, depth)
    db_con.close()


























