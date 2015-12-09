# coding=UTF-8

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup, UnicodeDammit

page_url = '/aqi/huludao-201510.html'
html = urlopen("http://www.tianqihoubao.com" + page_url)
bsObj = BeautifulSoup(html, "lxml", from_encoding="gb18030")



nameList = bsObj.find("table", {"class":"b"})
print(nameList.children)

first = True
for child in nameList.children:
    mchild = re.sub('\s','',str(child))
    if len(mchild) < 1:
        continue
    if first:
        title = re.split('<b>',mchild)
        title = [re.split('</b>',iunit)[0] for iunit in title]
        print(title)
        first = False
        continue
    nchild = re.split('<td>|<tdclass=\"aqi-lv[0-9]{1}\">',mchild)
    print(mchild)
    print(nchild)
    for item in nchild:
        if re.match('^>',item) is not None:
            nitem = re.split('<',re.split('>',item)[1])[0]
        else:
            nitem = re.split('<',item)[0]
        print(nitem)
    #nchild = re.search('(\>)[a-zA-Z0-9]+(\<)',mchild)
    #print(mchild)
    #print(nchild.group())

'''
for name in nameList:
    print(name)

nameList = bsObj.find("h4")
region = re.split('\d+',nameList.get_text())
print(region[0])'''
