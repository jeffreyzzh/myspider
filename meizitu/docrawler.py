# -*- coding: utf-8 -*-
#

import requests
from bs4 import BeautifulSoup
import os


class DoCrawl(object):
    def __init__(self):
        self.start_url = "http://www.mzitu.com/all"
        self.do_request = DoRequest()
        self.base_path = "/Users/Jeffrey/mm2"

    def do_mkdir(self, title):
        title = title.strip()
        isExists = os.path.exists(os.path.join(self.base_path, title))
        if not isExists:
            print('创建文件夹：', title)
            os.mkdir(os.path.join(self.base_path, title))
            return True
        else:
            # print('文件夹：', title, '已存在')
            return False

    def save_img(self, save_url, title):
        html = self.do_request.do_request(save_url)
        soup = BeautifulSoup(html.text, 'lxml')
        img_url = soup.find('div', class_='main-image').find('img')['src']
        print('crawl :', img_url)
        imgName = img_url[-9:]
        img = self.do_request.do_request(img_url)
        save_path = self.base_path + "/" + title + "/" + imgName
        with open(save_path, 'ab') as f:
            f.write(img.content)
        print(img_url, '保存成功')

    def get_every_mm(self, get_url, title):
        page_html = self.do_request.do_request(get_url)
        page_soup = BeautifulSoup(page_html.text, 'lxml')
        page_cont = page_soup.find('div', class_='pagenavi').find_all('a')[4]
        pagenum = page_cont.find('span').text
        for each in range(1, int(pagenum) + 1):
            crawl_url = get_url + '/' + str(each)
            print('保存图片：', crawl_url)
            self.save_img(crawl_url, title)
            break

    def do_main(self):
        start_html = self.do_request.do_request(self.start_url)
        all_a = BeautifulSoup(start_html.text, 'lxml').find("div", class_='all').find_all('a')
        # do_url = ''
        count = 1
        for a in all_a:
            title = a.get_text()
            do_url = a['href']
            self.do_mkdir(title)
            self.get_every_mm(do_url, title)
            if count == 10:
                break
            count += 1


class DoRequest(object):
    def __init__(self):
        self.content = ''

    def do_request(self, url):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        }
        self.content = requests.get(url, headers=headers)
        return self.content


if __name__ == '__main__':
    crawl = DoCrawl()
    crawl.do_main()
