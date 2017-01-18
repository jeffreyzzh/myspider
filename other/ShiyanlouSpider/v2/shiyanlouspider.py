# -*- coding: utf-8 -*-
# 2017/1/18
import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as e_c


def main():
    url = 'https://www.shiyanlou.com/'
    driver = webdriver.Chrome()
    driver.set_window_size(1800, 1000)
    driver.get(url)

    dosomething(driver)
    time.sleep(20)

    driver.close()


def get_user_info():
    try:
        info = json.load(open('password.txt'))
        username = info.get('username')
        password = info.get('password')
    except FileNotFoundError:
        username = input('input username:')
        password = input('input password:')
    return username, password


def dosomething(driver):
    try:
        username, password = get_user_info()
        driver.find_element_by_xpath('//a[@class="btn btn-default navbar-btn sign-in"]').click()

        WebDriverWait(driver, 300).until(
            e_c.presence_of_element_located((By.XPATH, '//*[@id="sign-modal"]/div/div/div/ul/li[1]/a')))
        time.sleep(1)

        login_name = driver.find_element_by_xpath('//*[@id="signin-form"]/form/div[1]/div/input')
        login_name.clear()
        login_name.send_keys(username)

        login_pwd = driver.find_element_by_xpath('//*[@id="signin-form"]/form/div[2]/div/input')
        login_pwd.clear()
        login_pwd.send_keys(password)

        login_pwd.send_keys(Keys.RETURN)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start = time.time()
    main()
    print('spider consumes for {:.6f} seconds'.format(time.time() - start))
