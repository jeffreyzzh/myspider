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

    def __del__(self):
        self.client.close()


if __name__ == '__main__':
    uc = UCstore()
