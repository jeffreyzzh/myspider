# -*- coding: utf-8 -*-
# 2017/4/1

import time
from weather_spider.spider_weather_dao import Weather, WeatherCity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from weather_spider.settings import *
import sqlalchemy


class Store:
    def __init__(self):
        conn_str = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
            MYSQL_USER,
            MYSQL_PWD,
            MYSQL_HOST,
            MYSQL_PORT,
            MYSQL_DB
        )
        engine = create_engine(conn_str)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def __del__(self):
        self.session.close()

    def insert(self, object):
        self.session.add(object)
        self.session.commit()

    def insert_batch(self, lists):
        self.session.add_all(lists)
        self.session.commit()

    def query_all(self, clazz):
        return self.session.query(clazz).all()

    def query_num_by_city(self, city):
        """
        采集天气，根据城市名查询ID
        :param city:
        :return:
        """
        city = self.session.query(WeatherCity).filter_by(scwc_name=city).first()
        if not city:
            return -1
        return city.get_num()

    def query_all_city_name(self):
        return self.session.query(WeatherCity.scwc_num, WeatherCity.scwc_name)

    def query_is_crawl(self, cityname, str_time):
        return self.session.query(Weather).filter(
            sqlalchemy.and_(Weather.scw_city == cityname, Weather.scw_time == str_time)).first()

    def get_50pull_data(self, count=50):
        update_time = time.strftime("%Y-%m-%d %H:%M:%S")
        """
        返回50条未pull的数据
        :return:
        """
        pulls = self.session.query(Weather).filter(Weather.scw_ispull == 0).limit(count).all()
        for each in pulls:
            self.session.query(Weather).filter(Weather.scw_id == each.scw_id).update(
                {'scw_ispull': 1, 'scw_pull_time': update_time})
        self.session.commit()
        return pulls

    def get_all_pull_data(self):
        update_time = time.strftime("%Y-%m-%d %H:%M:%S")
        """
        返回所有未pull的数据
        :return:
        """
        pulls = self.session.query(Weather).filter(Weather.scw_ispull == 0).all()
        for each in pulls:
            self.session.query(Weather).filter(Weather.scw_id == each.scw_id).update(
                {'scw_ispull': 1, 'scw_pull_time': update_time})
        self.session.commit()
        return pulls


if __name__ == '__main__':
    s = Store()
    # print s.query_num_by_city('巴黎')
    # for i in s.get_pull_data():
    #     print i
    for i in s.get_50pull_data():
        print(i)
