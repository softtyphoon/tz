




from news_spider import news_spider
from video_spider import video_spider



if __name__ == "__main__":
    print u'开始爬取咨询信息...'
    # 设置资讯的存储位置，必须以 \\ 结尾，分为绝对路径和相对路径
    #   c:\资讯\\     C:\咨询 目录下存放 txt，c:\资讯\图片 目录下存放图片
    #   咨询\         程序当前文件夹下的 资讯 目录存储 txt， 里面的 图片目录存放图片
    news_path = u'c:\资讯\\'
    # 设置视频目录，同上
    video_path = u'c:\视频\\'
    print u'游戏资讯的存放路径是：' + news_path
    a = news_spider(path = news_path)
    a.run()
    print u'开始爬取视频信息...'
    print u'视频信息的的存放路径是：' + video_path
    a = video_spider(path = video_path)
    a.run()
    pass
    









