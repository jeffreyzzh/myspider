# -*- coding: utf-8 -*-
# 2016/11/11 0011
# JEFF

import urllib.request
import urllib.error
import urllib.parse
import re
import rsa
import http.cookiejar
import base64
import json
import urllib
import binascii


class Launcher(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_encrypted_name(self):
        username_urllike = urllib.request.quote(self.username)
        username_encrypted = base64.b64encode(bytes(username_urllike, encoding='utf-8'))
        print(username_encrypted.decode('utf-8'))
        return username_encrypted.decode('utf-8')

    def get_login_args(self):
        """
        该函数用于模拟预登录过程,并获取服务器返回的 nonce , servertime , pub_key 等信息,用一个字典返回数据
        """
        url_part_1 = 'http://login.sina.com.cn/sso/login.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&'
        url_part_2 = self.get_encrypted_name()
        url_part_3 = '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'
        url = url_part_1 + url_part_2 + url_part_3
        json_pattern = re.compile('\((.*)\)')
        try:
            print(url)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            raw_data = response.read().decode('utf-8')
            json_data = json_pattern.search(raw_data).group(1)
            data = json.loads(json_data)
            return data
        except urllib.error as e:
            print(e.code)
            return None

    def get_encrypted_pw(self, data):
        rsa_e = 65537
        pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(self.password)
        key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
        pw_encrypted = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''
        passwd = binascii.b2a_hex(pw_encrypted)
        print(passwd)
        return passwd

    def enableCookies(self):
        # 建立一个cookies 容器
        cookie_container = http.cookiejar.CookieJar()
        # 将一个cookies容器和一个HTTP的cookie的处理器绑定
        cookie_support = urllib.request.HTTPCookieProcessor(cookie_container)
        # 创建一个opener,设置一个handler用于处理http的url打开
        opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        # 安装opener，此后调用urlopen()时会使用安装过的opener对象
        urllib.request.install_opener(opener)

    def build_post_data(self, raw):

        page1 = 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F'
        page2 = "http://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=http%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.14"

        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "useticket": "1",
            "pagerefer": page2,
            "vsnf": "1",
            "su": self.get_encrypted_name(),
            "service": "miniblog",
            "servertime": raw['servertime'],
            "nonce": raw['nonce'],
            "pwencode": "rsa2",
            "rsakv": raw['rsakv'],
            "sp": self.get_encrypted_pw(raw),
            "sr": "1280*800",
            "encoding": "UTF-8",
            "prelt": "77",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "META"
        }
        data = urllib.request.urlencode('utf-8').encode('utf-8')
        return data

    def login(self):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        self.enableCookies()
        data = self.get_login_args()
        post_data = self.build_post_data(data)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
        }
        try:
            request = urllib.request.Request(url=url, data=post_data, headers=headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('gbk')
            # print(html)
        except urllib.error as e:
            print(e.code)

        p = re.compile('location\.replace\(\'(.*?)\'\)')
        p2 = re.compile(r'"userdomain":"(.*?)"')

        try:
            login_url = p.search(html).group(1)
            print(login_url)
            request = urllib.request.Request(login_url)
            response = urllib.request.urlopen(request)
            page = response.read().decode('utf-8')
            print(page)
            login_url = 'http://weibo.com/' + p2.search(page).group(1)
            request = urllib.request.Request(login_url)
            response = urllib.request.urlopen(request)
            final = response.read().decode('utf-8')

            print("login success")
        except:
            print("login false")
            return 0


if __name__ == '__main__':
    l = Launcher('13674001454', 'aa6670620')
    l.login()
