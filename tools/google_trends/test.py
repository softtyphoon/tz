from pyGoogleTrendsCsvDownloader import pyGoogleTrendsCsvDownloader
import time
from random import randint

google_username = 'sxmman@126.com'
google_pass = 'zjjydqglp'

# Create the csv downloader object
downloader = pyGoogleTrendsCsvDownloader(google_username, google_pass)

# Wait some time to avoid blocking by google
time.sleep(randint(0, 5))
# http://www.google.com/trends/trendsReport?q=Pizza&export=1
# Attributes for the url
kwargs = {'q':'Pizza'}

downloader.get_csv(**kwargs)
