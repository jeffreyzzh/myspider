# -*- coding: utf-8 -*-
# 2017/1/23 0023
# JEFF
import time

from guazi3.tool import format_time_full
import mysql.connector as mysqlconn
import pymongo

conn = mysqlconn.connect(user='root', password='root', database='learnpy')

cursor = conn.cursor()
# cursor.execute('select * from guazi_items limit {},{}'.format(0, 100))
cursor.execute('select * from guazi_items')
values = cursor.fetchall()

info = ['title',
        'price',
        'since',
        'mileage',
        'gearbox',
        'emission_standard',
        'location',
        'owner',
        'description',
        'spider_time',
        'url']

item_list = []
for each in values:
    itemdict = {}
    for i in range(len(info)):
        itemdict[info[i]] = each[i + 1]
    itemdict['spider_time'] = format_time_full(int(itemdict['spider_time']))
    item_list.append(itemdict)

cursor.close()
conn.close()

if __name__ == '__main__':
    start = time.time()
    client = pymongo.MongoClient()
    db = client['guazi']
    coll = db['items']
    for each in item_list:
        coll.insert(each)
    print(time.time() - start)
