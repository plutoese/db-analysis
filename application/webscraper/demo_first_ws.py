# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pickle


pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://www.tianqihoubao.com"+pageUrl)
    bsObj = BeautifulSoup(html, "lxml")

    for link in bsObj.findAll("a", href=re.compile("^(/aqi/)[a-zA-Z]+(-)?[0-9]*(\.html)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)


getLinks("/aqi/")
F = open('E:/docs/pages.pkl', 'wb')
pickle.dump(pages, F)



