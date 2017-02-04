# -*- coding: utf-8 -*-
# 2017/1/24 0024
# JEFF

import time


def current_time_full():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def format_time_full(timex=None):
    if not timex:
        return current_time_full()
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timex))


def current_time_simple():
    return time.strftime('%Y-%m-%d')


def bak_mongodb(dbname, collname, newname):
    if not dbname or not collname or not newname:
        pass
    import pymongo
    client = pymongo.MongoClient()
    db = client[dbname]
    coll = db[collname]
    new_coll = db[newname]
    for i in coll.find({}, {'_id': 0}):
        new_coll.insert(i)


if __name__ == '__main__':
    print(format_time_full(1485144582))
    print(format_time_full())
    bak_mongodb('guazi', 'items', 'items2')
