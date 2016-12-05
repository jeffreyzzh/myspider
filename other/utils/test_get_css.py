# -*- coding: utf-8 -*-
# 2016/12/5

import os
import re

import lxml.html
import requests

base_path = os.path.abspath('.')

filename = '1.html'
css_name = '{}.css'
css_new_name = r'css\\{}.css'
css_file_name = base_path + '\\css\\{}.css'

with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

selector = lxml.html.fromstring(html)
css_list = selector.xpath('//link[@href]/@href')
c = 1
for css in css_list:
    css_url = str(css)
    if not css_url.endswith('.css'):
        continue
    # with open(css_file_name.format(c), 'w', encoding='utf-8') as f:
    #     f.write(requests.get(css).text)
    html = re.sub(css, css_new_name.format(c), html)
    c += 1

# re.sub('<title>\w+(实验楼)</title>')
a = re.search('<title>(.*?)</title>', html, re.S)
title = a.group(1)
new_title = re.sub('实验楼', 'Jeffrey', title)
html = re.sub(title, new_title, html)
# print(html)

js_list = re.findall('(<script src=.*?</script>)', html, re.S)
print(len(js_list))
for js in js_list:
    # print(type(js))
    print(js)
    new_js = '<!--{}-->'.format(js)
    print(new_js)
    # xxxx = re.compile(js)
    # html2 = re.sub(xxxx, new_js, html)
    html = html.replace(js, new_js)
print(html)

# new_html = 'new{}'.format(filename)
# new_html_path = os.path.join(base_path, new_html)
# with open(new_html_path, 'w', encoding='utf-8') as f:
#     f.write(html)
# print(html)
