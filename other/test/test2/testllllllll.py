# -*- coding: utf-8 -*-
# 2016/12/9

import requests
import re

with open(r"C:\Users\Administrator\Desktop\x.html", 'r', encoding='utf-8') as f:
    html = f.read()

js_count = 1
js_list = re.findall('<script src="(.*?)"></script>', html, re.S)
for js in js_list:
    with open("{}.js".format(js_count), 'wb') as f:
        f.write(requests.get(js).content)
    html = html.replace(js, '{}.js'.format(js_count))
    js_count += 1

css_count = 1
css_list = re.findall('<link rel="stylesheet" href="(.*?)">', html, re.S)
for css in css_list:
    with open("{}.css".format(css_count), 'wb')as f:
        f.write(requests.get(css).content)
    html = html.replace(css, '{}.css'.format(css_count))
    css_count += 1

# ![此处输入图片的描述](https://dn-anything-about-doc.qbox.me/document-uid8834labid1165timestamp1468333370769.png/wm)
img_count = 1
img_list = re.findall('!\[.*?\]\((.*?)\)', html, re.S)
for img in img_list:
    with open("{}.png".format(img_count), 'wb')as f:
        f.write(requests.get(img).content)
    html = html.replace(img, '{}.png'.format(img_count))
    img_count += 1

print(html)
with open('newhtml.html', 'w', encoding='utf-8') as f:
    f.write(html)
