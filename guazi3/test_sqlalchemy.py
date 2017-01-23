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
    emission_standard = Column(String())
