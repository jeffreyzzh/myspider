# -*- coding: utf-8 -*-
# 2016/12/6
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
WebDriverWait(driver=driver, 300).until(EC.presence_of_all_elements_located)
