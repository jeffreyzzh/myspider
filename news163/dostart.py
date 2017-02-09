# -*- coding: utf-8 -*-
# 2017/2/8
import time

import re
import requests
import json
from news163.log import Logger
from bs4 import BeautifulSoup


class News163Spider(object):
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

    URL = 'http://news.163.com/shehui/'
    AJAX_URL = 'http://temp.163.com/special/00804KVA/cm_shehui.js'
    AJAX_URLS = 'http://temp.163.com/special/00804KVA/cm_shehui_0{}.js'
    HOT_COMMENT_URL = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/hotList?limit=20'

    def __init__(self):
        self.logger = Logger().get_logger()

    def domain(self):
        resp = requests.get(self.URL)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        # 今日推荐
        totay_news = self.today_news(soup)

    def today_news(self, soup):
        infos = []
        if not soup or not isinstance(soup, BeautifulSoup):
            return infos
        news = soup.select('div.today_news a')
        for n in news:
            info = {
                'url': n.get('href'),
                'title': n.text
            }
            infos.append(info)
        return infos

    def ajax_news(self):
        urls = []
        news = self.ajax_parse(self.AJAX_URL)
        for i in range(2, 9):
            u = self.AJAX_URLS.format(i)
            urls.append(u)
            news2 = self.ajax_parse(u)
            news.extend(news2)
        return news

    def ajax_parse(self, url):
        cont = self.ajax_fetch(url)
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
            news.append(dict_info)
        return news

    def fetch(self, url, encoding):
        self.logger.info(url)
        try:
            r = requests.get(url, timeout=3)  # 在这里抓取页面
            r.encoding = encoding
            if not r.status_code == 404:
                return r.text
        except Exception as e:
            self.logger.error(e)
            return None

    def ajax_fetch(self, url):
        return self.fetch(url, 'gbk')

    def page_fetch(self, url):
        return self.fetch(url, 'utf-8')

    def new_comment(self, url):
        html = self.page_fetch(url)
        self.logger.info(html)

    def hot_comment(self, url):
        try:
            new_num = re.search('bbs/(.*?)\.html', url)
            r_url = self.HOT_COMMENT_URL.format(new_num.group(1))
            cont = self.page_fetch(r_url)
            dict_json = json.loads(cont)
            # 先判断是否没有评论
            if not dict_json['comments']:
                self.logger.info('url:{} no comments'.format(url))
                return
            result_info = dict()
            comment_list = []
            for k, v in dict_json['comments'].items():
                comment_info = dict()
                comment_info['content'] = v['content']
                comment_info['ip'] = v['ip']
                comment_info['vote'] = v['vote']
                comment_info['against'] = v['against']
                comment_info['commentId'] = v['commentId']
                comment_info['location'] = v['user']['location']
                comment_info['createTime'] = v['createTime']
                comment_info['news_url'] = url
                try:
                    comment_info['nickname'] = v['user']['nickname']
                except KeyError:
                    comment_info['nickname'] = 'niming'
                comment_list.append(comment_info)
            result_info['comments'] = comment_list
            try:
                result_info['newListSize'] = dict_json['newListSize']
            except KeyError:
                result_info['newListSize'] = len(comment_list)
            yield result_info
        except Exception as e:
            self.logger.error('url: {} has a problem'.format(url))
            self.logger.error(e)


if __name__ == '__main__':
    start = time.time()

    s = News163Spider()
    # s.ajax_news()
    # s.new_comment('http://comment.news.163.com/news_shehui7_bbs/CCQTHRHV0001875P.html')
    # s.hot_comment('http://comment.news.163.com/news_shehui7_bbs/CCQTHRHV0001875P.html')
    # a = s.hot_comment('http://comment.news.163.com/news_shehui7_bbs/CCQQK59U0001875P.html')
    # for each in a:
    #     print(each)
    news = s.ajax_news()
    for i in news:
        for each in s.hot_comment(i['commenturl']):
            s.logger.info(each)

    print('{0:.6f}'.format(time.time() - start))
