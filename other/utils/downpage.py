# -*- coding: utf-8 -*-
# 2016/12/4 0004
# JEFF

import requests
import re
import lxml.html
import os


class Downpage(object):
    def __init__(self):
        self.base_dir = r'C:\Users\Administrator\Desktop\dos'
        self.img_dir = '{}\\image'.format(self.base_dir)
        self.new_file_name = r'image\\{}.png'
        self.base_img_name = '{}.png'
        self.new_html = {}
        if not os.path.exists(self.img_dir.format(self.base_dir)):
            os.mkdir(self.img_dir)
            print('dir:"{}" init success...'.format(self.img_dir))

    def do_main(self):
        for parent, dirnames, filenames in os.walk(self.base_dir):
            i = 1
            for filename in filenames:
                print('处理的文件：{}'.format(filename))
                page_name = os.path.join(parent, filename)
                print('文件路径：{}'.format(page_name))
                if page_name.endswith("html"):
                    with open(page_name, 'rb') as f:
                        html = f.read().decode('utf-8')
                    selector = lxml.html.fromstring(html)
                    src = selector.xpath('//img/@src')
                    for each in src:
                        print(each)
                        # 保存图片到本地
                        print(self.base_img_name.format(i))
                        img_path = os.path.join(self.img_dir, self.base_img_name.format(i))
                        with open(img_path, 'wb') as f:
                            f.write(requests.get(each).content)
                        html = re.sub(each, self.new_file_name.format(i), html)
                        i += 1
                    new_html = 'new{}'.format(filename)
                    new_page_name = os.path.join(parent, new_html)
                    with open(new_page_name, 'w', encoding='utf-8') as f:
                        f.write(html)


if __name__ == '__main__':
    d = Downpage()
    d.do_main()
