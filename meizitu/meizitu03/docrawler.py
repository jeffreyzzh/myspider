# -*- coding: utf-8 -*-
# 2016/11/8
# author = JEFF

from bs4 import BeautifulSoup
from pymongo import MongoClient
from dodown import Download
import datetime
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

        client = MongoClient()
        db = client['meizutuxiezhenji']
        self.meizitu_collection = db['meizutu']
        self.title = ''
        self.url = ''
        self.img_urls = []

    def domain(self):
        html = self.request(self.start_url)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            href = a['href']
            print('开始保存', title)
            path = str(title).replace('?', '_')
            img_dir_path = self.mkdir(path)
            self.title = path
            self.url = href
            self.img_urls.clear()
            if self.meizitu_collection.find_one({'主题页面': href}):
                print('该页面已经爬取过..')
            else:
                self.html(href, img_dir_path)

    def request(self, url):
        return self.download.domain(url)

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
        crawl_count = 0
        for page in range(1, int(pagenum) + 1):
            page_url = href + '/' + str(page)
            crawl_count += 1
            self.img(page_url, img_dir_path, pagenum, crawl_count)

    def img(self, page_url, img_dir_path, pagenum, crawl_count):  ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.img_urls.append(img_url)
        self.save(img_url, img_dir_path)
        if int(pagenum) == crawl_count:
            post = {
                '标题': self.title,
                '主题页面': self.url,
                '图片地址': self.img_urls,
                '保存时间': datetime.datetime.now()
            }
            self.meizitu_collection.save(post)
            print('插入数据库成功')

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
