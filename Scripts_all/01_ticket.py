# -*- coding: utf-8 -*-
import os
import time
from PIL import ImageGrab
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def create_screenshot(time_wait):
    count = 0
    driver = webdriver.Firefox()
    driver.maximize_window()
    with open(file='input.txt', mode='r', encoding='utf-8') as file:
        for url in file:
            count += 1
            url = url.replace('\n', '')
            driver.get(url)
            time.sleep(time_wait)
            try:
                WebDriverWait(driver, 10)
            finally:
                screen_name = str(scr_name) + '_' + str(count)
                img = ImageGrab.grab()
                screenshot_name = 'scr/' + str(screen_name) + '.png'
                img.save(screenshot_name)
    driver.quit()


path = os.getcwd()
try:
    os.mkdir(path + r'\scr')
except FileExistsError:
    pass
scr_name = input('Введите название для скриншотов - ')
time_to_wait = int(input('Введите сколько секунд необходимо ждать после открытия сайта - (секунд) '))

create_screenshot(time_wait=time_to_wait)
