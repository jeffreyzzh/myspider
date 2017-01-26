# -*- coding: utf-8 -*-
# 2017/1/26 0026
# JEFF

import pymongo

client = pymongo.MongoClient()
db = client['data']
coll = db['test']

if __name__ == '__main__':
    for i in coll.find({'age': {'$exists': True}}):
        print(i)
        print('te' in i['name'])
