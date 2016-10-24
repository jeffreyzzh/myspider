# -*- coding: utf-8 -*-

from .items import QqtvcommentItem
from scrapy.conf import settings
import pymongo


class QqtvcommentPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db_name]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        comment = dict(item)
        self.post.insert(comment)
        return item
