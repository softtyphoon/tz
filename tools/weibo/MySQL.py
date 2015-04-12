
import MySQLdb

class MySQL():
    '''
      操作数据库类
    '''
    def __init__(self, host='localhost', user='root', pwd='123456', dbname='', port=3306):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.dbname = dbname
        self.port = port
        self.con = None

    def connet_mysql(self):
        if self.con is not None:
            self.con.close()
        
        try:
            self.con = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pwd, port=self.port)
            
        except:
            print 'Error: failed to connect mysql'
    
    def create_db(self):
        if self.con is  None:
            print 'Error: connect MYSql first'
        else:
            cur=self.con.cursor()
            cur.execute('create database if not exists python')
            self.con.select_db('python')
            # cur.execute('create table test(id int,info varchar(20))')

    def insert_data(self):
        cur=self.con.cursor()
        value=[1,u'好'.encode('gbk')]
        cur.execute('insert into test values(%s,%s)',value)
        print 'inserted'
        
    def query_table(self):
        cur=self.con.cursor()
        count=cur.execute('select * from test')
        print 'there has %s rows record' % count
        result=cur.fetchone()
        for i in result:
            print i
        
    def close_db(self):
        self.con.close()
        print 'closed'
    
if __name__ == "__main__":
    a = MySQL()
    a.connet_mysql()
    a.create_db()
    a.insert_data()
    a.query_table()
    a.close_db()
    
    
    
  







