# -*- coding: utf-8 -*-
# 2017/1/18
import time
import json
from other.ShiyanlouSpider.v2.shiyanlou_settings import spider_list
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as e_c


def main():
    url = 'https://www.shiyanlou.com/courses/?course_type=all&tag=Python&fee=all'
    driver = webdriver.Chrome()
    driver.get(url)

    login(driver)
    time.sleep(1)

    driver.find_element_by_css_selector(
        'body > div.container.layout.layout-margin-top > div > div.col-md-9.layout-body > div.content.position-relative > div.row > div:nth-child(4) > a > div.course-img > img').click()
    time.sleep(3)

    parse_course(driver)

    time.sleep(20)
    driver.close()


def parse_course(driver):
    pass


def get_user_info():
    try:
        info = json.load(open('password.txt'))
        username = info.get('username')
        password = info.get('password')
    except FileNotFoundError:
        username = input('input username:')
        password = input('input password:')
    return username, password


def login(driver):
    username, password = get_user_info()
    driver.find_element_by_xpath('//a[@class="btn btn-default navbar-btn sign-in"]').click()

    WebDriverWait(driver, 300).until(
        e_c.presence_of_element_located((By.XPATH, '//*[@id="sign-modal"]/div/div/div/ul/li[1]/a')))
    time.sleep(0.5)

    login_name = driver.find_element_by_xpath('//*[@id="signin-form"]/form/div[1]/div/input')
    login_name.clear()
    login_name.send_keys(username)

    login_pwd = driver.find_element_by_xpath('//*[@id="signin-form"]/form/div[2]/div/input')
    login_pwd.clear()
    login_pwd.send_keys(password)

    login_pwd.send_keys(Keys.RETURN)


def into_course(driver):
    driver.find_element_by_xpath('//*[@id="labs"]/div/div[4]/a[1]').click()
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")  # 向下滚动到页面底部


if __name__ == '__main__':
    start = time.time()
    main()
    print('spider consumes for {:.6f} seconds'.format(time.time() - start))
