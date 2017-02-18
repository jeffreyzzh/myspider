# -*- coding: utf-8 -*-
# 2017/2/10 0010
# JEFF
import re
from news163_2.tools.common_tools import DbTool
from news163_3.settings import CHANNEL_LIST


class URLmanager(object):
    regex_dict = {
        'filter_remark': re.compile('bbs/(.*?)\.html')
    }

    CRAWL_URLS = {
        'temp': {
            'channels': ['shehui', 'guoji', 'guonei'],
            'ajax_url': 'http://temp.163.com/special/00804KVA/cm_{}.js',
            'ajax_urls': 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js',
            'max': 8,
            'description': '普通频道，3个子频道：社会，国际，国内'
        },
        'sport': {
            'channels': ['index', 'allsports', 'cba', 'nba', 'china', 'world'],
            'ajax_url': 'http://sports.163.com/special/000587PR/newsdata_n_{}.js',
            'ajax_urls': 'http://sports.163.com/special/000587PR/newsdata_n_{}_0{}.js',
            'extra_urls': ['http://sports.163.com/special/000587PR/newsdata_n_index_10.js'],
            'max': 5,
            'description': '体育频道，6个子频道：首页，热点，CBA，NBA，国足，世界足球'
        },
        'ent': {
            'channels': ['index', 'star', 'movie', 'tv', 'show', 'music'],
            'ajax_url': 'http://ent.163.com/special/000380VU/newsdata_{}.js',
            'ajax_urls': 'http://ent.163.com/special/000380VU/newsdata_{}_0{}.js',
            'max': 8,
            'description': '娱乐频道，6个子频道：首页，明星，电影，电视剧，综艺，音乐'
        },
        'money': {
            'channels': ['index', 'stock', 'chanjing', 'finance', 'fund', 'licai', 'biz'],
            'ajax_url': 'http://money.163.com/special/002557S5/newsdata_idx_{}.js',
            'ajax_urls': 'http://money.163.com/special/002557S5/newsdata_idx_{}_0{}.js',
            'max': 8,
            'description': '财经频道，7个子频道：首页，股票，产经，金融，基金，理财，商业'
        },
        'tech': {
            'channels': ['datalist'],
            'ajax_url': 'http://tech.163.com/special/00097UHL/tech_{}.js',
            'ajax_urls': 'http://tech.163.com/special/00097UHL/tech_{}_0{}.js',
            'max': 3,
            'description': '科技频道'
        },
        'lady': {
            'channels': ['fashion', 'sense', 'travel', 'art', 'edu', 'baby'],
            'ajax_url': 'http://lady.163.com/special/00264OOD/data_nd_{}.js',
            'ajax_urls': 'http://lady.163.com/special/00264OOD/data_nd_{}_0{}.js',
            'max': 5,
            'description': '女性频道，6个子频道：时尚，情爱，旅游，艺术，教育，亲子'
        },
        'edu': {
            'channels': ['hot', 'liuxue', 'yimin', 'en', 'daxue', 'gaokao'],
            'ajax_url': 'http://edu.163.com/special/002987KB/newsdata_edu_{}.js',
            'ajax_urls': 'http://edu.163.com/special/002987KB/newsdata_edu_{}_0{}.js',
            'max': 3,
            'description': '教育频道，6个子频道：热点，留学，移民，外语，校园，高考'
        },

    }

    URL = 'http://news.163.com/shehui/'
    HOT_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/hotList?limit={}'
    NEW_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/newList?limit={}'

    def ajaxdict_by_crawl_channels(self, channels):
        """
        对普通新闻做特殊处理，每个子频道是一个独立的存储dict，
        其他的大频道对应一个存储dict
        :param channels: 频道列表
        :return: ajax_list_dict
        """
        result = dict()
        for channel in channels:
            if channel != 'temp':
                return_list = list()
                channelinfo = self.CRAWL_URLS.get(channel)
                if not channelinfo:
                    continue
                child_channels = channelinfo.get('channels')
                maxtimes = channelinfo.get('max')
                ajax_url = channelinfo.get('ajax_url')
                ajax_urls = channelinfo.get('ajax_urls')
                for x in child_channels:
                    return_list.append(ajax_url.format(x))
                    for y in range(2, maxtimes + 1):
                        return_list.append(ajax_urls.format(x, y))
                result[channel] = return_list
            else:
                channelinfo = self.CRAWL_URLS.get(channel)
                child_channels = channelinfo.get('channels')
                maxtimes = channelinfo.get('max')
                ajax_url = channelinfo.get('ajax_url')
                ajax_urls = channelinfo.get('ajax_urls')
                for x in child_channels:
                    list2 = list()
                    list2.append(ajax_url.format(x))
                    for y in range(2, maxtimes + 1):
                        list2.append(ajax_urls.format(x, y))
                    result[x] = list2
        return result

    def hotcomment_ajax_by_commenturl(self, commenturl, nums=40):
        new_num = re.search(self.regex_dict['filter_remark'], commenturl)
        return self.HOT_COMMENT_URL.format(new_num.group(1), nums)

    def newcomment_ajax_by_commenturl(self, commenturl, nums=10):
        new_num = re.search(self.regex_dict['filter_remark'], commenturl)
        return self.NEW_COMMENT_URL.format(new_num.group(1), nums)

    def commenturl_filterlist_by_channel(self, channel):
        channel_coll = DbTool.get_mongocoll_by_channel(channel)
        urls = channel_coll.find({}, {'commenturl': 1, '_id': 0})
        result_list = list()
        for i in urls:
            result_list.append(self.commenturl_filter_remark(i.get('commenturl')))
        return result_list

    def commenturl_filter_remark(self, commenturl):
        new_num = re.search(self.regex_dict['filter_remark'], commenturl)
        return new_num.group(1)


def geturlmanager():
    return URLmanager()


if __name__ == '__main__':
    m = geturlmanager()
    # channel_list = ['temp', 'lady']
    # s = m.ajaxdict_by_crawl_channels(channels=channel_list)
    # for k, v in s.items():
    #     print(k)
    #     print(v)

    comment_url = 'http://comment.sports.163.com/sports2_bbs/CDI6AGOT0005877U.html'
    i = m.hotcomment_ajax_by_commenturl(comment_url, 40)
    print(i)
    k = m.newcomment_ajax_by_commenturl(comment_url)
    print(k)


    # channel = 'shehui'
    # filter_list = m.commenturl_filterlist_by_channel(channel)
    # print(filter_list)