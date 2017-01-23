# -*- coding: utf-8 -*-
# 2017/1/23 0023
# JEFF

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = 'guazi_items'

    id = Column(String(20), primary_key=True)
    title = Column(String(50))
    price = Column(String(10))
    since = Column(String(10))
    mileage = Column(String(10))
    gearbox = Column(String(5))
    emission_standard = Column(String(5))
    location = Column(String(5))
    owner = Column(String(5))
    description = Column(String(200))
    spider_time = Column(String(20))
    spider_url = Column(String(50))


engine = create_engine('mysql+mysqlconnector://root:root@192.168.1.112:3306/guazi_items')

DBSession = sessionmaker(bind=engine)

session = DBSession()
item = session.query(Item).filter(Item.id == '5').one()

print(item.owner)
session.close()
