

import urllib2
import re
import sys




_url = 'http://onlinelibrary.wiley.com/documentcitationdownloadformsubmit'
_header = {
        'Host':'onlinelibrary.wiley.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        'Referer':'http://onlinelibrary.wiley.com/doi/10.1029/2012GL053876/abstract',
        'Connection':'keep-alive'
    }

# _data = 'doi=10.1029%252F2012GL053876&fileFormat=ENDNOTE&hasAbstract=CITATION_AND_ABSTRACT'
_data = 'doi=10.1029%252FGL001i008p00329&fileFormat=ENDNOTE&hasAbstract=CITATION_AND_ABSTRACT'
# def file_download(url, header, data=None):
def file_download(doi, path, fn):
    '''
      download file from specific url
    '''
    url = 'http://onlinelibrary.wiley.com/documentcitationdownloadformsubmit'
    header = {
        'Host':'onlinelibrary.wiley.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate',
        # 'Referer':'http://onlinelibrary.wiley.com/doi/10.1029/2012GL053876/abstract',
        'Connection':'keep-alive'
    }
    dooi = doi.replace('/', '%252F')
    data = 'doi=' + dooi + '&fileFormat=ENDNOTE&hasAbstract=CITATION_AND_ABSTRACT'
    fnn = path + fn
    opener = urllib2.OpenerDirector()
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    req = urllib2.Request(url)
    for (name, val) in header.items():
        req.add_header(name, val)
    req.add_header('Referer', 'http://onlinelibrary.wiley.com/doi/'+doi+'/abstract')

    if data is not None:
        # req.add_header(name, val)
        req.add_data(data)

    try:
        r = opener.open(req, timeout = 60)
    except:
        print 'failed'
        opener.close()
        r.close()
        sys.exit(0)

    # cd = r.info().get('Content-Disposition')
    # p = re.compile(r'(?<=filename=).*')
    # fn = p.search(cd).group()
    # if p is None:
        # return False
    if r.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(r.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = r.read()

    file = open(fnn, 'w+')
    file.write(data)
    file.close()
    print 'write file '+doi+' done!'

def get_urls():
    '''
      get all destiny URLs from http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1944-8007/issues?activeyear2011
    '''

def get_doi():
    '''
      get DOI string from specific web page
    '''

if __name__ == "__main__":
    # test code
    # file_download(_url, _header, _data)
    file_download('10.1029%252FGL001i008p00329', '', 'acd.enw')
    sys.exit(0)
    # end of test code

    start_url = 'http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1944-8007/issues/fragment?activeYear=2015&SKIP_DECORATION=true'
    # first, get all volume&issue urls
    webs = get_urls()
    for a in webs:
        # get all DOIs in every url
        b = get_doi()
        for c in b:
            # then, download enw for every DOI
            file_download()

    print 'Done'






