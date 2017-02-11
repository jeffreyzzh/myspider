# -*- coding: utf-8 -*-
# 2017/2/10 0010
# JEFF
import re


class URLmanager(object):
    URL = 'http://news.163.com/shehui/'
    AJAX_URL = 'http://temp.163.com/special/00804KVA/cm_{}.js'
    AJAX_URLS = 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js'
    HOT_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/hotList?limit=20'

    def __init__(self):
        pass

    def ajax_list_by_channel(self, channel='shehui'):
        urls = list()
        urls.append(self.AJAX_URL.format(channel))
        for i in range(2, 9):
            urls.append(self.AJAX_URLS.format(channel, i))
        return urls

    def hotcomment_ajax_by_commenturl(self, commenturl):
        new_num = re.search('bbs/(.*?)\.html', commenturl)
        return self.HOT_COMMENT_URL.format(new_num.group(1))

    def ajxa_news(self):
        pass


def geturlmanager():
    return URLmanager()


if __name__ == '__main__':
    m = URLmanager()
    print(m.ajax_list_by_channel('guonei'))
