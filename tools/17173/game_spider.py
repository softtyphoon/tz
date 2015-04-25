




from news_spider import news_spider
from video_spider import video_spider



if __name__ == "__main__":
    print u'开始爬取咨询信息...'
    a = news_spider()
    a.run()
    print u'开始爬取视频信息...'
    a = video_spider(path = u'c:\\视频\\')
    a.run()
    pass
    









