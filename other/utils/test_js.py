# -*- coding: utf-8 -*-
# 2016/12/9

import re

import requests

with open(r"C:\Users\Administrator\Desktop\a.html", 'r', encoding='utf-8') as f:
    html = f.read()

print(html)

js_list = re.findall('<script src="(.*?)"></script>', html, re.S)
print(js_list)

js_count = 1
for each in js_list:
    with open('{}.js'.format(js_count), 'wb') as f:
        f.write(requests.get(each).content)
    html = html.replace(each, '{}.js'.format(js_count))
    js_count += 1

# print(html)
with open("new.html", 'w', encoding='utf-8') as f:
    f.write(html)
