# -*- coding: utf-8 -*-
# 2016/11/8
# author = JEFF

import requests
import random
import time
import re


class Download(object):
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.ip_list = self.get_ip_list()

    def get_ip_list(self):
        iplist = []
        html = requests.get("http://haoip.cc/tiqu.htm")
        iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)  # findall返回的是个list
        for ip in iplistn:
            i = re.sub('\n', '', ip)  # re.sub 是re模块替换的方法，这儿表示将\n替换为空
            iplist.append(i.strip())
        return iplist

    def domain(self, url, timeout=3.5, proxy=None, num_retries=6):
        ua = random.choice(self.user_agent_list)
        headers = {'User-Agent': ua}
        if proxy == None:
            try:
                return requests.get(url, headers=headers, timeout=timeout)
            except:
                if num_retries > 0:
                    print(u'获取网页出错，10S后将获取倒数第：', num_retries, u'次')
                    time.sleep(10)
                    return self.domain(url, num_retries=num_retries - 1)
                else:
                    print('开始使用代理')
                    time.sleep(10)
                    ip = ''.join(str(random.choice(self.ip_list)))
                    proxy = {'http', ip}
                    return self.domain(url, proxy=proxy, )
        else:
            try:
                ip = ''.join(str(random.choice(self.ip_list)))
                proxy = {'http', ip}
                return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            except:
                if num_retries > 0:
                    print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                    time.sleep(10)
                    ip = ''.join(str(random.choice(self.ip_list)))
                    proxy = {'http': ip}
                    print(u'当前代理是：', proxy)
                    return self.domain(url, proxy, num_retries - 1)
                else:
                    print(u'代理也不好使了！取消代理')
                    return self.domain(url)


if __name__ == '__main__':
    url = "http://music.163.com"
    download = Download()
    response = download.domain(url, 3.5)
    print(response.status_code)
    print(response.cookies)
    print(response.apparent_encoding)
    print(response.encoding)
    print(response.headers)
    # print(response.content)
    # print(response.text)
    print(response.elapsed)
    print(response.history)
    print(response.request)
