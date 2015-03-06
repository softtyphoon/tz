


a = u'LNsdsdsdfSA'
if a[0:2].lower() == u'ln':
  print 'dfdfdf'

fn = open(u'1.txt')
num = 0
ln = 0
lx = 0
lm = 0
for line in fn.readlines():
  if line[0:2].lower() == u'ln':
    ln = ln + 1
  if line[0:2].lower() == u'lx':
    lx = lx + 1
  if line[0:2].lower() == u'lm':
    lm = lm + 1
  print line[0:2].lower()
  print len(line[0:2])

print u'ln: %d'%(ln)
print u'lx: %d'%(lx)
print u'lm: %d'%(lm)

print ln
print lx
print lm