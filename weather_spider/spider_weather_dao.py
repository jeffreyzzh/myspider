# -*- coding: utf-8 -*-
# 2017/4/1

from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
import time

Base = declarative_base()


class Weather(Base):
    __tablename__ = 'scb_crawler_weather'

    scw_id = Column(Integer, primary_key=True)
    scw_city = Column(String(20))
    scw_time = Column(String(20))
    scw_weather = Column(String(20))
    scw_temp_h = Column(String(20))
    scw_temp_l = Column(String(20))
    scw_wind = Column(String(50))
    scw_create_time = Column(Date)
    scw_crawl_time = Column(Date)
    scw_ispull = Column(Integer)
    scw_pull_time = Column(Date)


class WeatherCity(Base):
    __tablename__ = 'scb_crawler_weather_citys'

    scwc_id = Column(Integer, primary_key=True)
    scwc_name = Column(String(20))
    scwc_num = Column(Integer)
    scwc_create_time = Column(Date)
    scwc_crawl_time = Column(Date)

    def get_num(self):
        return self.scwc_num


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
