# -*- coding: utf-8 -*-
# 2017/1/13

# 测试
from guazi.common_getset_info import GetAndSet

if __name__ == '__main__':
    gs = GetAndSet()
    area, car, cartype = gs.get_mongo_colls()
    cars = car.find()
    for each in cars:
        for k, v in each.items():
            # print(k, v)
            has = cartype.find({k: v})
            if list(has):
                print(k, v)
