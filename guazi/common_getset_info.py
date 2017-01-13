# -*- coding: utf-8 -*-
# 2017/1/12

import logging
import random
import pymongo
import time
from guazi.common_parse import ParsePage

base_url = 'https://www.guazi.com/{}/{}'


class GetAndSet(object):
    def __init__(self, dbname='guazi', collname='default_info'):
        areacoll = '_area'
        areacoll2 = '_area2'
        carcoll = '_car'
        cartypecoll = '_car_type'
        client = pymongo.MongoClient()
        self.db = client[dbname]
        self.area = self.db[collname + areacoll]
        self.area2 = self.db[collname + areacoll2]
        self.car = self.db[collname + carcoll]
        self.cartype = self.db[collname + cartypecoll]

    def set_area(self, area1, area2=None):
        self.area.insert(area1)
        if area2:
            self.area2.insert(area2)

    def set_car(self, car):
        self.car.insert(car)

    def set_car_type(self, car_type):
        self.cartype.insert(car_type)

    def get_area(self):
        return self.area.find_one()

    def get_car(self):
        return self.car.find_one()

    def get_car_type(self):
        pass

    def get_all_info(self):
        return self.area.find_one(), self.area2.find_one(), self.car.find_one()

    def get_type_bycar_net(self, car="丰田"):
        car_dict = self.get_car()
        pass

    def get_mongo_colls(self):
        return self.area, self.car, self.cartype


if __name__ == '__main__':
    gs = GetAndSet()
    page = ParsePage()
    car_dict = gs.get_car()
    area, car, cartype = gs.get_mongo_colls()
    # for c in car_dict:
    #     if c == '_id':
    #         continue
    #     print(c)
    #     dict = page.get_type_bycar(c, car_dict)
    #     gs.set_car_type(dict)
    #     print(dict)
    #     sec = random.randint(15, 20)
    #     print('sleep {}'.format(sec))
    #     time.sleep(sec)

    for each in car.find():
        for k, v in each.items():
            has = cartype.find({k: v})
            if not list(has):
                if k == '_id':
                    continue
                print(k)
                dict = page.get_type_bycar(k, car_dict)
                gs.set_car_type(dict)
                print(dict)
                sec = random.randint(15, 20)
                print('sleep {}'.format(sec))
                time.sleep(sec)
