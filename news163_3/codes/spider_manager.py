# -*- coding: utf-8 -*-
# 2017/2/10 0010
# JEFF
import re
from news163_2.tools.common_tools import DbTool


class URLmanager(object):
    URL = 'http://news.163.com/shehui/'
    HOT_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/hotList?limit=20'

    # 普通新闻
    AJAX_URL = 'http://temp.163.com/special/00804KVA/cm_{}.js'
    AJAX_URLS = 'http://temp.163.com/special/00804KVA/cm_{}_0{}.js'  # max 8

    # 体育相关
    SPORT_AJAX_URL = 'http://sports.163.com/special/000587PR/newsdata_n_index.js'
    SPORT_AJAX_URLS = 'http://sports.163.com/special/000587PR/newsdata_n_index_0{}.js'  # max 9
    SPORT_AJAX_M_URL = 'http://sports.163.com/special/000587PR/newsdata_n_index_10.js'

    ALLSPORT_AJAX_URL = 'http://sports.163.com/special/000587PR/newsdata_n_allsports.js'
    ALLSPORT_AJAX_URLS = 'http://sports.163.com/special/000587PR/newsdata_n_allsports_0{}.js'  # max 5

    # NBA_AJAX_URL = 'http://sports.163.com/special/000587PK/newsdata_nba_index.js'
    # NBA_AJAX_URLS = 'http://sports.163.com/special/000587PK/newsdata_nba_index_0{}.js'  # max 9
    # NBA_AJAX_M_URL = 'http://sports.163.com/special/000587PK/newsdata_nba_index_10.js'

    SPORT_CBA_AJXA_URL = 'http://sports.163.com/special/000587PR/newsdata_n_cba.js'
    SPORT_CBA_AJXA_URLS = 'http://sports.163.com/special/000587PR/newsdata_n_cba_0{}.js'  # max 5

    SPORT_NBA_AJXA_URL = 'http://sports.163.com/special/000587PR/newsdata_n_nba.js'
    SPORT_NBA_AJXA_URLS = 'http://sports.163.com/special/000587PR/newsdata_n_nba_0{}.js'  # max 5

    SPORT_GNFB_AJAX_URL = 'http://sports.163.com/special/000587PR/newsdata_n_china.js'
    SPORT_GNFB_AJAX_URLS = 'http://sports.163.com/special/000587PR/newsdata_n_china_0{}.js'  # max 5

    SPORT_GJFB_AJAX_URL = 'http://sports.163.com/special/000587PR/newsdata_n_world.js'
    SPORT_GJFB_AJAX_URLS = 'http://sports.163.com/special/000587PR/newsdata_n_world_0{}.js'  # max 5

    # 娱乐相关
    YULE_AJAX_URL = 'http://ent.163.com/special/000380VU/newsdata_index.js'
    YULE_YL_AJAX_URLS = 'http://ent.163.com/special/000380VU/newsdata_index_0{}.js'  # max 9
    YULE_YL_AJAX_M_URL = 'http://ent.163.com/special/000380VU/newsdata_index_10.js'

    YULE_MX_URL = 'http://ent.163.com/special/000380VU/newsdata_star.js'
    YULE_MX_URLS = 'http://ent.163.com/special/000380VU/newsdata_star_0{}.js'  # max9
    YULE_MX_M_URL = 'http://ent.163.com/special/000380VU/newsdata_star_10.js'

    YULE_MOVIE_URL = 'http://ent.163.com/special/000380VU/newsdata_movie.js'
    YULE_MOVIE_URLS = 'http://ent.163.com/special/000380VU/newsdata_movie_0{}.js'  # max 9
    YULE_MOVIE_M_URL = 'http://ent.163.com/special/000380VU/newsdata_movie_10.js'

    YULE_TV_URL = 'http://ent.163.com/special/000380VU/newsdata_tv.js'
    YULE_TV_URLS = 'http://ent.163.com/special/000380VU/newsdata_tv_0{}.js'  # max 9
    YULE_TV_M_URL = 'http://ent.163.com/special/000380VU/newsdata_tv_10.js'

    YULE_ZY_URL = 'http://ent.163.com/special/000380VU/newsdata_show.js'
    YULE_ZY_URLS = 'http://ent.163.com/special/000380VU/newsdata_show_0{}.js'  # max 9
    YULE_ZY_M_URL = 'http://ent.163.com/special/000380VU/newsdata_show_10.js'

    YULE_MUSIC_URL = 'http://ent.163.com/special/000380VU/newsdata_music.js'
    YULE_MUSIC_URLS = 'http://ent.163.com/special/000380VU/newsdata_music_0{}.js'  # max 9
    YULE_MUSIC_M_URL = 'http://ent.163.com/special/000380VU/newsdata_music_10.js'

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
