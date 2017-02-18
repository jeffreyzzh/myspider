# -*- coding: utf-8 -*-
# 2017/2/18
# author = JEFF

import pymongo
import re

client = pymongo.MongoClient()

db = client['163news']
shehuicoll = db['shehui_coll']
guoneicoll = db['guonei_coll']
guojicoll = db['guoji_coll']


def commenturl_filter_remark(commenturl):
    new_num = re.search('bbs/(.*?)\.html', commenturl)
    return new_num.group(1)


def update_mongo(coll):
    lists = coll.find({}, {'commenturl': 1})
    for each in lists:
        remark = commenturl_filter_remark(each['commenturl'])
        coll.update({'_id': each['_id']}, {'$set': {'filter_remark': remark}})


if __name__ == '__main__':
    update_mongo(guojicoll)
    update_mongo(guoneicoll)
    update_mongo(shehuicoll)
