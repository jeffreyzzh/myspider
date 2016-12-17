# -*- coding: utf-8 -*-
# 16/12/3

import pymongo

# client = pymongo.MongoClient('192.168.1.112', 27017)
client = pymongo.MongoClient()
db = client['data']
coll = db['test']

test = {
    'name': 'test'
}

coll.insert(test)
