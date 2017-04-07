# -*- coding: utf-8 -*-
# 2017/3/30

import pymongo


class UCstore(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        db = self.client['uc']
        self.coll = db['spl']

    def insert(self, data):
        self.coll.insert(data)

    def insert_list(self, datalist):
        for each in datalist:
            self.insert(each)

    def last_pos(self):
        pos = self.coll.find().sort('_pos', pymongo.DESCENDING).limit(1)
        try:
            return pos[0]['_pos']
        except Exception:
            return -1

    def coll_object(self):
        return self.coll

    def update_content(self, content_dict):
        self.coll.update({'_id': content_dict['_id']}, {'$set': {'content': content_dict}})

    def __del__(self):
        self.client.close()
