# -*- coding: utf-8 -*-
# 2017/2/10 0010
# JEFF
import re
from news163_2.tools.common_tools import DbTool


class URLmanager(object):
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
            'channels': ['index', 'stock', 'chanjing', 'finance', 'fund ', 'licai ', 'biz'],
            'ajax_url': 'http://money.163.com/special/002557S5/newsdata_idx_{}.js',
            'ajax_urls': 'http://money.163.com/special/002557S5/newsdata_idx_{}_0{}.js',
            'max': 9,
            'description': '财经频道，7个子频道：首页，股票，产经，金融，基金，理财，商业'
        },
        'tech': {
            'channels': [],
            'ajax_url': '',
            'ajax_urls': '',
            'max': 0,
            'description': ''
        },
        'lady': {
            'channels': [],
            'ajax_url': '',
            'ajax_urls': '',
            'max': 0,
            'description': ''
        },
        'edu': {
            'channels': [],
            'ajax_url': '',
            'ajax_urls': '',
            'max': 0,
            'description': ''
        },

    }

    URL = 'http://news.163.com/shehui/'
    HOT_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/hotList?limit=20'

    # 普通新闻
    # shehui guoji guonei
    AJAX_URL = 'http://temp.163.com/special/00804KVA/cm_{}.js'
    AJAX_URLS = 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js'  # max 8

    # 体育频道
    # index (max 9)
    # allsports cba nba china world (max 5)
    SPORT_AJAX_URL = 'http://sports.163.com/special/000587PR/newsdata_n_{}.js'
    SPORT_AJAX_URLS = 'http://sports.163.com/special/000587PR/newsdata_n_{}_0{}.js'  # max 9
    SPORT_AJAX_M_URL = 'http://sports.163.com/special/000587PR/newsdata_n_index_10.js'

    # NBA_AJAX_URL = 'http://sports.163.com/special/000587PK/newsdata_nba_index.js'
    # NBA_AJAX_URLS = 'http://sports.163.com/special/000587PK/newsdata_nba_index_0{}.js'  # max 9
    # NBA_AJAX_M_URL = 'http://sports.163.com/special/000587PK/newsdata_nba_index_10.js'

    # 娱乐频道
    # index star movie tv show music (max 8)
    YULE_AJAX_URL = 'http://ent.163.com/special/000380VU/newsdata_{}.js'
    YULE_YL_AJAX_URLS = 'http://ent.163.com/special/000380VU/newsdata_{}_0{}.js'

    # 财经频道
    # index stock(股票) chanjing(产经) finance(金融) fund(基金) licai(理财) biz(商业)(max 9)
    MONEY_AJXA_URL = 'http://money.163.com/special/002557S5/newsdata_idx_{}.js'
    MONEY_AJXA_URLS = 'http://money.163.com/special/002557S5/newsdata_idx_{}_0{}.js'

    # 科技频道
    # (max 3)
    KEJI_AJAX_URL = 'http://tech.163.com/special/00097UHL/tech_datalist.js'
    KEJI_AJAX_URLS = 'http://tech.163.com/special/00097UHL/tech_datalist_0{}.js'

    # 女人频道
    # fashion sense(情爱) travel art edu baby (max 5)
    LADY_AJAX_URL = 'http://lady.163.com/special/00264OOD/data_nd_{}.js'
    LADY_AJAX_URLS = 'http://lady.163.com/special/00264OOD/data_nd_{}_0{}.js'

    # 教育频道
    # hot liuxue yimin en(外语) daxue gaokao (max 3)
    EDU_AJAX_URL = 'http://edu.163.com/special/002987KB/newsdata_edu_{}.js'
    EDU_AJAX_URLS = 'http://edu.163.com/special/002987KB/newsdata_edu_{}_0{}.js'

    # 汽车频道 房产频道 健康频道
    # todo （同步页面）

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

    def commenturl_filterlist_by_channel(self, channel):
        channel_coll = DbTool.get_mongocoll_by_channel(channel)
        urls = channel_coll.find({}, {'commenturl': 1, '_id': 0})
        result_list = list()
        for i in urls:
            result_list.append(i.get('commenturl'))
        return result_list


def geturlmanager():
    return URLmanager()


if __name__ == '__main__':
    m = URLmanager()
    # print(m.ajax_list_by_channel('guonei'))
    for i in m.commenturl_filterlist_by_channel('shehui'):
        print(i)
    print(len(m.commenturl_filterlist_by_channel('shehui')))
