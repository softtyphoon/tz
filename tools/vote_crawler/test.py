

# import re

# # a = '\"ht:/df/d/asd/zxc\"'
# a = '"dfgf"jhj"sdsd"'
# # a = '\"adsfd\"'
# print a

# # '<a href="(.*)">(.*)</a>'
# # p = re.compile(r'"(.*)"$')
# p = re.compile(r'"(\w+)"')
# # p = re.compile(r'\"[a-z]\"')
# # print p.search(a).group()
# print p.findall(a)

print u'\u7f8e'.encode('gbk')
# print u'\u7f8e'.encode('unicode-escape').encode('gbk')
d = '\u7f8e'.encode('unicode-escape')
print d
print eval(d)
print eval('\u7f8e')












