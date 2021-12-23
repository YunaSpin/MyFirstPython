import requests
from bs4 import BeautifulSoup
import re
from faker import Faker


def getHTML(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
        }
        r = requests.get(url, headers=headers)

        r.encoding = 'utf-8'
        print(r.text)
        soup = BeautifulSoup(r.text, "lxml")

        titleandhref = soup.find_all('a', {'class': 'title'})
        for i in titleandhref:
            print(i.string)
    except:
        print("error")


getHTML('https://www.acfun.cn/rank/list/?cid=-1&pcid=-1&range=DAY')
