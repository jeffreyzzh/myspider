# -*- coding: utf-8 -*-
# 2017/1/12

import pymongo
from guazi2.tool.time_tool import log_current_date

base_url = 'https://www.guazi.com/{}/{}'


class GetAndSet(object):
    def __init__(self, dbname='guazi', collname='default_info'):
        areacoll = '_area'
        areacoll2 = '_area2'
        carcoll = '_car'
        cartypecoll = '_car_type'
        urls = '{}_urls'.format(log_current_date())
        items = '{}_items'.format(log_current_date())
        client = pymongo.MongoClient()
        self.db = client[dbname]
        self.area = self.db[collname + areacoll]
        self.area2 = self.db[collname + areacoll2]
        self.car = self.db[collname + carcoll]
        self.cartype = self.db[collname + cartypecoll]
        self.carurls = self.db[urls]
        self.items = self.db[items]

    def set_area(self, area1, area2=None):
        """插入地区"""
        self.area.insert(area1)
        if area2:
            self.area2.insert(area2)

    def set_car(self, car):
        """插入车型"""
        self.car.insert(car)

    def set_car_type_one(self, car, page_object):
        """确定要插入一个品牌的车型信息"""
        self.cartype.insert(page_object.get_type_bycar(car, self.get_car()))

    def set_car_type(self, page_object):
        """插入所有品牌的车型信息"""
        cars = self.get_car()
        for k in cars:
            if k == '_id':
                continue
            dict = page_object.get_type_bycar(k, cars)
            self.cartype.insert(dict)

    def get_gd_area(self):
        """返回所有广东城市"""
        return {'佛山': 'foshan',
                '深圳': 'sz',
                '广州': 'gz',
                '珠海': 'zhuhai',
                '东莞': 'dg',
                '中山': 'zhongshan',
                '江门': 'jiangmen',
                '汕头': 'shantou',
                '惠州': 'huizhou'}

    def get_area(self):
        """获取地区 area1:{'深圳': 'sz'}"""
        return self.area.find_one()

    def get_car(self):
        """获取品牌"""
        return self.car.find_one()

    def get_car_type(self):
        """获取所有车型、品牌"""
        cartypes = {}
        cars = self.get_car()
        for k, v in cars.items():
            if k == '_id':
                continue
            cartype = self.cartype.find({k: v})
            for typex in cartype:
                for nk, nv in typex.items():
                    if nk == '_id' or nk == k:
                        continue
                    cartypes[nk] = nv
        return cartypes

    def get_type_bycar(self, car='丰田'):
        """根据品牌获取车型"""
        cartypes = {}
        cars = self.get_car()
        c = cars.get(car)
        if not c:
            car = '丰田'
            c = 'toyota'
        t = self.cartype.find({car: c})
        for each in t:
            for k, v in each.items():
                if k == '_id' or k == car:
                    continue
                cartypes[k] = v
        return cartypes
        # return cartypes

    def get_all_info(self):
        """获取地区x2，品牌，车型DICT"""
        return self.area.find_one(), self.area2.find_one(), self.car.find_one(), self.get_car_type()

    def get_mongo_colls(self):
        """获取芒果连接"""
        return self.area, self.car, self.cartype

    def get_mongo_dayurls(self):
        """URL mongo coll object"""
        return self.carurls

    def get_mongo_dayitems(self):
        """
        ITEMS mongo coll object
        :return:
        """
        return self.items


if __name__ == '__main__':
    gs = GetAndSet()
    a, b, c, d = gs.get_all_info()
    print(a)
    print(b)
    print(c)
    print(d)
    print()
    x = gs.get_type_bycar('本田')
    print(x)
