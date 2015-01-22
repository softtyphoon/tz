

import argparse


_ascii = None
_hex = None
_fn = None

def main():
  global _ascii
  global _hex
  global _fn
  print _ascii
  print _hex
  print _fn





if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='convert HEX < === > ASCII')
  parser.add_argument('-ascii', dest='ascii', help='ASCII')
  parser.add_argument('-hex', dest='hex', help='HEX', action='store_true')
  parser.add_argument('-f', type=str, required=False, metavar='file', dest='fn', help='file name')
  _ascii = parser.parse_args().ascii
  _hex = parser.parse_args().hex
  _fn = parser.parse_args().fn
  if _ascii is None and _hex is None:
    print 'no argments input'
    print _fn
  else:
    main()
