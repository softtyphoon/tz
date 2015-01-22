
# try:
  # import xml.etree.cElementTree as ETk
# except ImportError:
import xml.etree.ElementTree as ET

import argparse

_fn = None

def xml_parser(fn):     # one depth
  tree = ET.parse('test.xml')
  root = tree.getroot()
  ay = dict()
  for sub in root:
    for ssub in sub:
      # print ', '.join(['%s:%s' % item for item in ssub.__dict__.items()])
      ay[ssub.attrib['name']] = ssub.text
  return ay


def main():
  global _fn
  print _fn
  a = xml_parser(_fn)
  print a


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='XML parser')
  parser.add_argument('-f', type=str, required=True, metavar='file', dest='fn', help='file name')
  _fn = parser.parse_args().fn
  main()