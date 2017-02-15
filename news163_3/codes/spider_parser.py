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
        keywords = list()
        for key in o_keywords:
            try:
                key = key.replace(' ', '')
                k_infos = key.split('\n,')
                n_infos = []
                for each in k_infos:
                    each = each.replace('${type}', 'news.163.com')
                    each_dict = json.loads(each)
                    n_infos.append(each_dict)
                keywords.append(n_infos)
            except Exception as e:
                self.logger.error(e)

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

    def parser_hotcomment(self, cont, url):
        if not cont:
            return None
        try:
            dict_json = json.loads(cont)
            result_info = dict()
            comment_list = list()
            if dict_json.get('code') == '40106':
                return None
            if dict_json.get('message') == 'Thread is closed':
                return None
            if not dict_json.get('comments'):
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
                comment_info['nickname'] = v.get('user').get('nickname')
                comment_list.append(comment_info)
            result_info['comments'] = comment_list
            result_info['newListSize'] = dict_json.get('newListSize') if dict_json.get('newListSize') else len(
                comment_list)
            return result_info
        except Exception as e:
            self.logger.log(e)
            self.logger.error('url: {} has a problem'.format(url))
            return None


def getparser():
    return URLparser()


if __name__ == '__main__':
    print(1)
