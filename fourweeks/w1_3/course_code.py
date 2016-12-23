# -*- coding: utf-8 -*-
# 2016/12/23

from bs4 import BeautifulSoup
import requests

url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())
title = soup.select('div.property_title > a')

print(title)
