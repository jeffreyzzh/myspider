# -*- coding: utf-8 -*-
# 2017/1/18

import lxml.html
from bs4 import BeautifulSoup as bs

with open('content.txt', 'rb') as f:
    html = f.read().decode()

html = lxml.html.fromstring(html)
name = html.xpath('//*[@id="sign-modal"]/div/div')
print(len(name))
# html = bs(html, 'lxml')
# alls = html.select('a[href="#signin-form"]')
# print(len(alls))

# driver.execute_script("window.scrollBy(0,200)","")  #向下滚动200px
# driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")  #向下滚动到页面底部
