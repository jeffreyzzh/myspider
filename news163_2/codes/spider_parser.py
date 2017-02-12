# -*- coding: utf-8 -*-
# 2017/2/10 0010
# JEFF
import json
import re

from news163_2.codes.spider_base import BaseClass
from news163_2.tools.common_tools import TimeTool


class URLparser(object):
    regex_dict = {
        'cont': re.compile('(\[.*\])', re.S),
        'titles': re.compile('"title":"(.*?)"', re.S),
        'docurls': re.compile('"docurl":"(.*?)"', re.S),
        'commenturls': re.compile('"commenturl":"(.*?)"', re.S),
        'timeums': re.compile('"tienum":(.*?),', re.S),
        'tlinks': re.compile('"tlink":"(.*?)"', re.S),
        'labels': re.compile('"label":"(.*?)"', re.S),
        'o_keywords': re.compile('"keywords":\[\s*(.*?)\s*\],', re.S),
        'times': re.compile('"time":"(.*?)"', re.S),
        'newstypes': re.compile('"newstype":"(.*?)"', re.S),
        'channelnames': re.compile('"channelname":"(.*?)"', re.S)
    }

    def __init__(self):
        self.logger = BaseClass.getlogger()

    def parse_ajax_channel(self, cont):
        if not cont:
            return None
        cont = re.search('(\[.*\])', cont.strip(), re.S).group()
        titles = re.findall(self.regex_dict['titles'], cont)
        docurls = re.findall(self.regex_dict['docurls'], cont)
        commenturls = re.findall(self.regex_dict['commenturls'], cont)
        timeums = re.findall(self.regex_dict['timeums'], cont)
        tlinks = re.findall(self.regex_dict['tlinks'], cont)
        labels = re.findall(self.regex_dict['labels'], cont)
        o_keywords = re.findall(self.regex_dict['o_keywords'], cont)
        times = re.findall(self.regex_dict['times'], cont)
        newstypes = re.findall(self.regex_dict['newstypes'], cont)
        channelnames = re.findall(self.regex_dict['channelnames'], cont)
        keywords = []
        for key in o_keywords:
            key = key.replace(' ', '')
            k_infos = key.split('\n,')
            n_infos = []
            for each in k_infos:
                each = each.replace('${type}', 'news.163.com')
                each_dict = json.loads(each)
                n_infos.append(each_dict)
            keywords.append(n_infos)

        news = []
        for title, docurl, commenturl, timeum, tlink, label, keyword, time, newstype, channelname in zip(
                titles, docurls, commenturls, timeums, tlinks, labels, keywords, times, newstypes, channelnames
        ):
            dict_info = {
                'title': title,
                'docurl': docurl,
                'commenturl': commenturl,
                'timeum': timeum,
                'tlink': tlink,
                'label': label,
                'keyword': keyword,
                'time': time,
                'newstype': newstype,
                'channelname': channelname
            }
            # for each in self.hot_comment(commenturl):
            #     dict_info['comment'] = each
            news.append(dict_info)
        return news

    def parser_hotcomment(self, cont, j):
        if not cont:
            return None
        dict_json = json.loads(cont)
        # 先判断是否没有评论
        if len(dict_json) <= 2:
            return None
        comment_list = list()
        if not dict_json['comments']:
            return None
        for k, v in dict_json['comments'].items():
            comment_info = dict()
            comment_info['content'] = v['content']
            comment_info['ip'] = v['ip']
            comment_info['vote'] = v['vote']
            comment_info['against'] = v['against']
            comment_info['commentId'] = v['commentId']
            comment_info['location'] = v['user']['location']
            comment_info['createTime'] = v['createTime']
            try:
                comment_info['nickname'] = v['user']['nickname']
            except KeyError:
                comment_info['nickname'] = 'niming'
            comment_list.append(comment_info)
        j['hotcomment_list'] = comment_list
        try:
            j['hotcomment_size'] = dict_json['newListSize']
        except KeyError:
            j['hotcomment_size'] = len(comment_list)
        j['spider_time'] = TimeTool.current_time()
        return j


def getparser():
    return URLparser()


if __name__ == '__main__':
    print(1)
