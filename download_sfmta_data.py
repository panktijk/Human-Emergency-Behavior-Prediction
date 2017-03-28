import urllib2
from bs4 import BeautifulSoup, SoupStrainer
from ftplib import FTP

ftp = FTP('avl-data.sfmta.com')
ftp.login()
ftp.cwd('avl_data/avl_raw')
files_list = ftp.nlst()
for f in files_list:
    if '2012.csv' in f.lower():
        ftp.retrbinary("RETR {}".format(f), open(f, "wb").write)
        print("downloaded {}".format(f))
ftp.quit()