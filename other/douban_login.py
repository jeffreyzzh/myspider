# -*- coding: utf-8 -*-
# 2016/12/2

import requests
import re


class Douban(object):
    def __init__(self):
        self.login_url = 'https://accounts.douban.com/login'
        self.user_url = 'https://www.douban.com/people/{}/'
        self.email = ''
        self.password = ''
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
        }
        self.session = requests.Session()

    def get_data(self, email, password):
        return {
            'source': None,
            'redir': 'https://www.douban.com/',
            'form_email': email,
            'form_password': password,
            'remember': 'on',
            'login': '登录'
        }

    def do_main(self):
        account = input('输入帐号：')
        password = input('输入密码：')
        data = self.get_data(account, password)
        html = self.session.post(self.login_url, headers=self.header).content.decode()
        captcha_url = re.findall('id="captcha_image" src="(.*?)"', html, re.S)  # 获取验证码url
        if captcha_url:  # 有验证码
            captcha_img = captcha_url[0]
            captcha_id = re.findall('name="captcha-id" value="(.*?)"', html, re.S)[0]  # 获取验证码ID
            # 下载图片
            with open('captcha.png', 'wb') as f:
                f.write(requests.get(captcha_img).content)
            captcha_solution = input('captcha code is:')
            data['captcha-solution'] = captcha_solution
            data['captcha-id'] = captcha_id
        result = self.session.post(self.login_url, data=data, headers=self.header).content
        print('login success...')
        while True:
            keyword = input('输入用户名：')
            if keyword == 'exit':
                print('exit success...')
                break
            user_info = self.session.get(self.user_url.format(keyword)).content
            print(re.findall('title>(.*?)</title', user_info.decode(), re.S)[0])


if __name__ == '__main__':
    d = Douban()
    d.do_main()
