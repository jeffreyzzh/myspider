# -*- coding: utf-8 -*-
# 2017/1/13

from guazi.common_getset_info import GetAndSet

base_url = 'https://www.guazi.com/{}/{}'


class PageUrl(object):
    def __init__(self):
        self.page = GetAndSet()
        self.area1, self.area2, self.car, self.cartype = self.page.get_all_info()

    def find_area_by_name(self, area_name='广州'):
        """根据中文名获取地区代号, 默认为广州"""
        area = self.area1.get(area_name)
        return area if area else 'gz'

    def find_car_by_name(self, car_name='丰田'):
        """根据中文名获取地区代号, 默认为丰田"""
        name = self.car.get(car_name)
        return name if name else 'toyota'

    def get_path(self, area='广州', car='丰田'):
        """根据地区，车型条件返回URL"""
        return base_url.format(self.find_area_by_name(area_name=area), self.find_car_by_name(car_name=car))

    def get_path_bycartype(self, area='广州', car='丰田', cartype='凯美瑞'):
        """根据地区，车型（品牌）条件返回URL"""
        car_name = self.find_car_by_name(car)
        car_type = self.cartype.get(car_name).get(cartype)
        return base_url.format(self.find_area_by_name(area_name=area), car_type if car_type else car_name)


if __name__ == '__main__':
    url = PageUrl()
    # print(url.get_path('珠海', '福特'))
    # print(url.get_path())
    print(url.get_path_bycartype())
    print(url.get_path_bycartype('佛山', '福特', '蒙迪欧'))
