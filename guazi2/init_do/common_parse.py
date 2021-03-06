# -*- coding: utf-8 -*-
# 17/1/1

import time

import lxml.html
import requests
from bs4 import BeautifulSoup

start_url = 'https://www.guazi.com/gz'
car_url = 'https://www.guazi.com/gz/richan'
base_url = 'https://www.guazi.com/{}/{}'
"""
base_url {0}: area / {1}: car type
"""

"""
foshan,
gz,
jiangmen
"""

"""
toyata,
honda
toyota-markx,
kaimeirui,
hanlanda,
siborui
"""


def get_all_area_set():
    areas = set()
    resp = requests.get(start_url)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    alls = soup.select('div.all-city a')
    for each in alls:
        area = each.get('href')
        area = str(area).strip()
        areas.add(area)
    return areas


class ParsePage(object):
    def __init__(self):
        self.start_url = 'https://www.guazi.com/gz'
        self.car_url = 'https://www.guazi.com/gz/richan'
        self.base_url = 'https://www.guazi.com/{}/{}'

    # def __parse_page(self, url, count=1):
    #     print('!!!!!!!!!!!!')
    #     if count >= 5:
    #         print(555555555555555555555555555555555555555)
    #         return None
    #     try:
    #         resp = requests.get(url, headers=get_ua_dict(), timeout=5)
    #         print(resp.status_code)
    #         if count >= 2:
    #             print(resp.text)
    #         return resp.text
    #     except Exception as e:
    #         print(e)
    #         time.sleep(15)
    #         self.__parse_page(url, count=count + 1)

    def get_car(self):
        car = {}
        response = requests.get(self.start_url)
        cont = response.text
        selector = lxml.html.fromstring(cont)
        alls = selector.xpath('//td//a[@data-gzlog]')
        for each in alls:
            name_cn = each.text
            path = each.get('href')
            new_path = path.split('/')[2]
            car[name_cn] = new_path
        return car

    def get_type_bycar(self, car="丰田", car_dict=None):
        car_type = {}
        if not car_dict:
            print('requests get dict...')
            car_dict = self.get_car()
        value = car_dict.get(car)
        url = self.base_url.format('gz', value)
        print(url)
        c_type = {}
        # cont = self.__parse_page(url)
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        cont = resp.text
        if cont is None:
            return {
                car: value,
                value: None
            }
        selector = lxml.html.fromstring(cont)
        alls = selector.xpath('/html/body/div[5]/div[1]/div[1]/dl[2]/dd/div/a[@data-gzlog]')
        for each in alls:
            type = each.text.strip()
            url = each.get('href').split('/')[2]
            c_type[type] = url
        car_type[value] = c_type
        car_type[car] = value
        return car_type

    def get_area_dict(self):
        """area1:{'深圳': 'sz'} area2:{'sz': '深圳'}"""
        area1 = {}
        area2 = {}
        resp = requests.get(self.start_url)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        alls = soup.select('div.all-city a')
        for each in alls:
            k = each.text.strip()
            v = str(each.get('href')).replace('/', '')
            area1[k] = v
            area2[v] = k
        return area1, area2

    def get_all_info(self):
        area1 = {}
        area2 = {}
        car = {}
        resp = requests.get(self.car_url)
        soup = BeautifulSoup(resp.content.decode(), 'lxml')
        alls = soup.select('div.all-city a')
        for each in alls:
            k = each.text.strip()
            v = str(each.get('href')).split('/')[1]
            area1[k] = v
            area2[v] = k

        selector = lxml.html.fromstring(resp.content.decode())
        cars = selector.xpath('//span[@class="brand-all z30"]//a[@data-gzlog]')
        for each in cars:
            name_cn = each.text.strip()
            path = each.get('href')
            new_path = path.split('/')[2]
            car[name_cn] = new_path

        return area1, area2, car


if __name__ == '__main__':
    page = ParsePage()
    a, b, c = page.get_all_info()
    #
    # print(a)
    # print(b)
    # print(c)
    car_type = page.get_type_bycar("大众", c)
    print(car_type)
