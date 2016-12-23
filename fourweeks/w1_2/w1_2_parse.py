# -*- coding: utf-8 -*-
# 2016/12/23

import os
from bs4 import BeautifulSoup

"""
标题，价格，描述，图片，评分
"""

current = os.path.abspath('.')
html_path = os.path.join(current, 'web/new_index.html')
print(os.path.exists(html_path))

with open(html_path, 'r') as f:
    html = f.read()

data_list = []

soup = BeautifulSoup(html, 'lxml')
imgs = soup.select('body > div.main-content > ul > li > img')
titles = soup.select('body > div.main-content > ul > li > div.article-info > h3 > a')
cates = soup.select('body > div.main-content > ul > li > div.article-info > p.meta-info')
descs = soup.select('body > div.main-content > ul > li > div.article-info > p.description')
rates = soup.select('body > div.main-content > ul > li > div.rate > span')

# print(imgs, titles, cates, desc, rates, sep='\n---------------------\n')
for img, title, cate, desc, rate in zip(imgs, titles, cates, descs, rates):
    info = {
        'title': title.get_text(),
        'img': img.get('src'),
        'cate': list(cate.stripped_strings),
        'desc': desc.get_text(),
        'rate': rate.get_text()
    }
    data_list.append(info)

for data in data_list:
    print(data, end='\n\n')
