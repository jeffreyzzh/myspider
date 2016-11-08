# -*- coding: utf-8 -*-
# 2016/11/8
# author = JEFF

from bs4 import BeautifulSoup
from meizitu.meizitu02.dodown import Download
import time
import os


class DoCrawl(object):
    def __init__(self):
        self.start_url = "http://www.mzitu.com/all"
        self.base_path = "F:\mm"
        self.base_txt = self.base_path + "\crawlloggig.txt"
        self.download = Download()
        # 创建工作文件夹
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)

    def domain(self):
        html = self.request(self.start_url)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            href = a['href']
            print('开始保存', title)
            path = str(title).replace('?', '_')
            img_dir_path = self.mkdir(path)
            self.html(href, img_dir_path)

    def request(self, url):
        return self.download.domain(url)
        # return requests.get(url, headers=headers)

    def mkdir(self, path):
        path = path.strip()
        img_dir_path = os.path.join(self.base_path, path)
        if not os.path.exists(img_dir_path):
            os.makedirs(img_dir_path)
            with open(self.base_txt, 'a') as w:
                w.write(path + ' ' + time.ctime() + '\n')
        return img_dir_path

    def html(self, href, img_dir_path):
        html = self.request(href)
        page_num = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('a')[4]
        pagenum = page_num.find('span').text
        for page in range(1, int(pagenum) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url, img_dir_path)

    def img(self, page_url, img_dir_path):  ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url, img_dir_path)

    def save(self, img_url, img_dir_path):  ##这个函数保存图片
        name = img_url[-9:]
        img = self.request(img_url)
        save_path = img_dir_path + '\\' + name
        with open(save_path, 'ab') as f:
            f.write(img.content)
        print(img_url, '保存成功', time.ctime())


if __name__ == '__main__':
    docrawl = DoCrawl()
    docrawl.domain()
