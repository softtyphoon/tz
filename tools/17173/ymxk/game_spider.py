




from news_spider import news_spider
from video_spider import video_spider
import re
import sys

def custom_encode(strings):
    temp_str = strings
    while True:
        try:
            pass
            temp_str.encode('gbk')
        except:
            info = sys.exc_info()
            pat = re.compile(r'u\d+')
            res = pat.findall(repr(info[1]))
            if len(res) == 0:
                return temp_str
            else:
                a = u'\\u' + u''.join(res[0][1:])
                a = 'u\'' + a + '\''
                a = eval(a)
                temp_str = temp_str.replace(a, u'')
                continue
            pass
        return temp_str
        pass

if __name__ == "__main__":
    news_url = 'http://www.gamersky.com/news/Special/dmc5/'
    hb_url = u'http://www.gamersky.com/handbook/Special/dmc5/'
    video_url = 'http://tag.gamersky.com/v/2245.html'
    video_url = 'http://v.gamersky.com/game/news/'
    print u'开始爬取咨询信息...'
    # 设置资讯的存储位置，必须以 \\ 结尾，分为绝对路径和相对路径
    #   c:\资讯\\     C:\咨询 目录下存放 txt，c:\资讯\图片 目录下存放图片
    #   咨询\         程序当前文件夹下的 资讯 目录存储 txt， 里面的 图片目录存放图片
    news_path = u'c:\资讯\\'
    # 设置攻略/视频目录，同上
    hb_path = u'c:\攻略\\'
    video_path = u'c:\视频\\'
    print u'游戏资讯的存放路径是：' + news_path
    a = news_spider(url = news_url, path = news_path, type = 0)
    a.run()
    del a
    print u'\n开始爬取游戏攻略'
    print u'游戏攻略的存放路径是：' + hb_path
    a = news_spider(url = hb_url, path = hb_path, type = 1)
    a.run()
    del a
    print u'\n开始爬取视频信息...'
    print u'视频信息的的存放路径是：' + video_path
    a = video_spider(url = video_url, path = video_path)
    a.run()
    pass
    









