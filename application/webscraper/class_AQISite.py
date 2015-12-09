# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from application.webscraper.class_SiteScraper import SiteScraper
import pickle
from lib.database.class_Database import Database

class AQISite:
    """定期抓取空气后天网站的空气污染数据

    """
    def __init__(self,website='http://www.tianqihoubao.com'):
        self.site_scraper = SiteScraper(website)
        self.data = []
        self.db = Database()
        self.con = self.db.connect('internetDB', 'AQI')

    def daily_aqi_data(self,url_pages):
        """抓取每天的空气污染指数

        :param str page: 城市空气污染指数页面
        :return:
        """
        for page in url_pages:

            if re.match("^(/aqi/)[a-zA-Z]+(-)[0-9]*(\.html)",page) is None:
                continue

            html = urlopen("http://www.tianqihoubao.com" + page)
            bsObj = BeautifulSoup(html, "lxml", from_encoding="gb18030")

            # 获取城市名称
            city_title = bsObj.find("h4")
            city_name = re.split('\d+',city_title.get_text())[0]

            # 获取空气污染数据
            table_list = bsObj.find("table", {"class":"b"})
            # 设定标识符，第一次为真
            first = True

            for child in table_list.children:
                child_str = re.sub('\s','',str(child))

                if len(child_str) < 1:
                    continue

                if first:
                    title = re.split('<b>',child_str)
                    title = [re.split('</b>',iunit)[0] for iunit in title]
                    var_name = title[1:]
                    first = False
                    continue

                aqi_data = []
                td_data_list = re.split('<td>|<tdclass=\"aqi-lv[0-9]{1}\">',child_str)
                for td_data in td_data_list:
                    if re.match('^>',td_data) is not None:
                        aqi_single_data = re.split('<',re.split('>',td_data)[1])[0]
                    else:
                        aqi_single_data = re.split('<',td_data)[0]
                    aqi_data.append(aqi_single_data)

                api_data = aqi_data[1:]
                a_data = dict(zip(var_name,api_data))
                a_data['city'] = city_name
                print(a_data)
                self.insertDB(a_data)


    def insertDB(self,record):
        new_record = dict()
        for key in record:
            value = record[key]
            if '.' in key:
                key = re.sub('\.','',key)
            if re.match('^\d+$',value) is not None:
                new_record[key] = int(value)
            elif re.match('^\d+(\.)\d*$',value) is not None:
                new_record[key] = float(value)
            else:
                new_record[key] = value
        print(new_record)
        self.con.insert_one(new_record)


if __name__ == '__main__':
    aqi_site = AQISite()

    F = open('E:/docs/pages.pkl', 'rb')
    pages = pickle.load(F)
    pages = list(pages)
    demo_pages = pages
    print(demo_pages)
    aqi_site.daily_aqi_data(demo_pages)

