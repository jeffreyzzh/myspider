# -*- coding: utf-8 -*-
# 17/1/1

import requests
from bs4 import BeautifulSoup

start_url = 'https://www.guazi.com/gz'
base_url = 'https://www.guazi.com/{}/{}/'
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


"""
areas = get_all_area_set()


def find_area_by_kedworld(*args):
    area = ''
    for each in args:
        area += str(each)
    if area in areas:
        return area
    else:
        area = ''
        for each in args:
            i = str(each)[0:1]
            area += i
        return area


k = find_area_by_kedworld('guang', 'zhou')
print(k)
"""


def get_area_dict():
    """{'深圳': 'sz'}"""
    area = {}
    resp = requests.get(start_url)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    alls = soup.select('div.all-city a')
    for each in alls:
        area[each.text.strip()] = str(each.get('href')).replace('/', '')
    return area


def get_area_dict2():
    """{'sz': '深圳'}"""
    dict = get_area_dict()
    area = {}
    for k, v in dict.items():
        area[v] = k
    return area


def find_area_by_kedworld(area_name):
    areas = get_area_dict()
    area = areas.get(area_name)
    return area if area else 'gz'


if __name__ == '__main__':
    # area = find_area_by_kedworld('傻不拉唧')
    # print(area)
    pass
