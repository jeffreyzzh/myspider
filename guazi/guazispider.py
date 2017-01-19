# -*- coding: utf-8 -*-
# 2017/1/19

from guazi.parse.parse_page import CarUrlParse
from guazi.db.common_getset_info import GetAndSet
from guazi.init_do.common_parse import ParsePage

# p = CarUrlParse('https://www.guazi.com/gz/dazhong/')
# p.do_main()
# print(p.get_linkscount())


if __name__ == '__main__':
    gs = GetAndSet()
    page = ParsePage()
    area1, area2, cars, cartypes = gs.get_all_info()
    cars2 = {}
    for k, v in cars.items():
        cars2[v] = k
    for k, v in cartypes.items():
        if not v:
            carname = cars2.get(k)
            print(carname)
            car_type = page.get_type_bycar(carname, cars)
            print(car_type)
            # car_type = page.get_type_bycar(k, cars)
            # print(car_type)
