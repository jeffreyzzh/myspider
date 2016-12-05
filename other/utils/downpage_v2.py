# -*- coding: utf-8 -*-
# 2016/12/4 0004
# JEFF

import requests
import re
import lxml.html
import os

import time


class Downpage(object):
    def __init__(self):
        self.do_dir = input("输入桌面上要进行下载的文件夹名称：")
        self.base_dir = r'C:\Users\Administrator\Desktop\{}'.format(self.do_dir)
        self.img_dir = '{}\\image'.format(self.base_dir)
        self.base_img_name = '{}.png'
        self.new_file_name = r'image\\{}.png'
        # self.new_html = {}
        self.base_css_name = '{}.css'
        self.css_dir = '{}\\css'.format(self.base_dir)
        self.new_css_name = r'css\\{}.css'
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)
            print('dir:"{}" init success...'.format(self.img_dir))
        if not os.path.exists(self.css_dir):
            os.mkdir(self.css_dir)
            print('dir:"{}" init success...'.format(self.css_dir))

    def do_main(self):
        for parent, dirnames, filenames in os.walk(self.base_dir):
            i = 1
            c = 1
            for filename in filenames:
                page_name = os.path.join(parent, filename)
                if page_name.endswith("html"):
                    with open(page_name, 'rb') as f:
                        html = f.read().decode('utf-8')
                    selector = lxml.html.fromstring(html)
                    # 图片处理
                    src = selector.xpath('//img/@src')
                    for each in src:
                        # print(each)
                        # 保存图片到本地
                        print(self.base_img_name.format(i))
                        img_path = os.path.join(self.img_dir, self.base_img_name.format(i))
                        with open(img_path, 'wb') as f:
                            f.write(requests.get(each).content)
                        # 修改网页中的图片引用地址
                        html = re.sub(each, self.new_file_name.format(i), html)
                        i += 1
                    # css文件处理
                    css_list = selector.xpath('//link[@href]/@href')
                    for css in css_list:
                        css_url = str(css)
                        if not css_url.endswith('.css'):
                            continue
                        # print(css_file_name.format(c))
                        # 保存css文件到本地
                        css_path = os.path.join(self.css_dir, self.base_css_name.format(c))
                        print(css_path)
                        with open(css_path, 'w', encoding='utf-8') as f:
                            f.write(requests.get(css).text)
                        # 修改网页中的css文件引用地址
                        html = re.sub(css, self.new_css_name.format(c), html)
                        c += 1
                    # 处理html页面其他内容
                    # 标题
                    title = re.search('<title>(.*?)</title>', html, re.S).group(1)
                    # new_title = re.sub('实验楼', 'Jeffrey', title)
                    new_title = title.replace('实验楼', 'Jeffrey')
                    # html = re.sub(title, new_title, html)
                    html = html.replace(title, new_title)
                    # JS
                    js_list = re.findall('(<script src=.*?</script>)', html, re.S)
                    for js in js_list:
                        new_js = '<!--{}-->'.format(js)
                        html = html.replace(js, new_js)
                    new_html = 'new{}'.format(filename)
                    new_page_name = os.path.join(parent, new_html)
                    with open(new_page_name, 'w', encoding='utf-8') as f:
                        f.write(html)


if __name__ == '__main__':
    d = Downpage()
    start_time = time.time()
    d.do_main()
    end_time = time.time()
    print('time:{}'.format(end_time - start_time))
