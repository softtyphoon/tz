import mechanize # other imports omitted for simplicity
import cookielib
import csv
import StringIO

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

response = br.open('https://accounts.google.com/ServiceLogin?hl=en&continue=https://www.google.com/')
forms = mechanize.ParseResponse(response)
form = forms[0]
form['Email'] = 'sxmman@126.com'
form['Passwd'] = 'zjjydqglp'
response = br.open(form.click())

Result = br.open("http://www.google.com/trends/trendsReport?q=nba&export=1")
print Result.read()
CSVcontent = csv.reader(StringIO(Result.read()))
print CSVcontent