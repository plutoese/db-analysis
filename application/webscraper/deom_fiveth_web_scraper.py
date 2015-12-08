# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html,"lxml")
for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])