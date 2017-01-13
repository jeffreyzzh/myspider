# -*- coding: utf-8 -*-
# 2017/1/12

import pymongo
import time
from guazi.common_parse import ParsePage


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


if __name__ == '__main__':
    gs = GetAndSet()
    page = ParsePage()
    a1, a2, c = gs.get_all_info()
    for each in c.keys():
        if each == '_id':
            break
        print(each)
        car_type = page.get_type_bycar(each)
        print(car_type)
    # area1, area2, car = page.get_all_info()
    # gs.set_area(area1, area2)
    # gs.set_car(car)

    # area1, area2, car = gs.get_all_info()
    # a = list(area1.keys())
    # print('惠州' in a)
