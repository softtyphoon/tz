





fn = open(u'ttt.txt')
count = 0;
for ct in fn.readlines():
  a = ct + u'hello'
  fn.writeline(a)
  count = count + 1
  if count == 10:
    break