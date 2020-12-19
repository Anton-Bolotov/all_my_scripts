import time
import os
import random
import shutil

from selenium import webdriver  # pip install selenium
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup  # pip install bs4
import requests  # pip install requests
from PIL import Image  # pip3 install Pillow

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=options)

url = str(input('Please insert link to the manga - '))
download_all = str(input('Please select. Download all pages the manga ? - Y/n '))
zip_archive = str(input('Please select. Create a zip archive ? - Y/n '))
to_gray = str(input('Please select. Monochrome images ? - Y/n '))
full_name_img = str(input('Please select. Full name images ? - Y/n '))
time_to_sleep = int(input('Please enter your sleep time - '))

print('\nThe download will start soon!')

if download_all == 'Y':
    if 'mintmanga' in url:
        url_accept = url[:url.find('/vol')] + '?mtr=1'
    else:
        if '?mtr=1' in url:
            url_accept = url[:url.find('/vol')] + '?mtr=1'
        else:
            url_accept = url[:url.find('/vol')]

    driver.get(url_accept)

    try:
        time.sleep(random.uniform(0.5, 1.0))
        driver.find_element_by_xpath('//*[@id="mangaBox"]/div[2]/div[1]/div[1]/div[3]/a').click()
    except NoSuchElementException:
        time.sleep(random.uniform(0.5, 1.0))
        driver.find_element_by_xpath('//*[@id="mangaBox"]/div[2]/div[1]/div[1]/div[2]/a').click()
else:
    driver.get(url)

count = 0
path = ''
title_name = ''
number_page_name = ''
bad_chars = ['/', '\\', '*', ':', '?', '|', '"', '<', '>', '.', ',', ]

while True:
    try:
        source_page = BeautifulSoup(driver.page_source, 'html.parser')
        title_name = source_page.find('a', attrs={'class': 'manga-link'}).text
        for bad_char in bad_chars:
            if bad_char in title_name:
                title_name = title_name.replace(bad_char, '')
        path = os.getcwd() + '\\' + title_name
        break
    except AttributeError:
        continue

try:
    os.mkdir(path)
    print(f'\nFolder named "{title_name}" was created successfully!\n')
except FileExistsError:
    pass

while True:
    time.sleep(time_to_sleep)
    source_page = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        page_name = str(source_page.find('h1').text)
        if full_name_img == 'Y':
            for bad_char in bad_chars:
                if bad_char in page_name:
                    page_name = page_name.replace(bad_char, '')

        else:
            number_page_name = ''
            for chair_page in page_name.split(' '):
                if chair_page.isdigit():
                    number_page_name += chair_page + '-'
            page_name = number_page_name

        screenshot_url = source_page.find('img', attrs={'id': 'mangaPicture'})['src']

    except AttributeError:
        continue
    except TypeError:
        break

    if len(page_name) >= 51:
        page_name = page_name[:50]
        if page_name[-1] == ' ':
            page_name = page_name[:-1]

    path_screen = os.getcwd() + '\\' + title_name + '\\' + page_name

    try:
        os.mkdir(path_screen)
        print(f'\nFolder named "{page_name}" was created successfully!\n')
        count = 0
    except FileExistsError:
        pass

    if full_name_img == 'Y':
        scr_name = path_screen + '\\' + str(count) + '_' + page_name
    else:
        scr_name = path_screen + '\\' + number_page_name + str(count)

    count += 1

    try:
        with open(f'{scr_name}.jpg', mode='wb') as create_screen:
            r = requests.get(screenshot_url)
            create_screen.write(r.content)

        if to_gray == 'Y':
            scr = Image.open(f'{scr_name}.jpg')
            grayscale = scr.convert('L').save(f'{scr_name}.jpg')

        print(f'Successfully downloaded images - {count}.')

    except FileNotFoundError:
        err_scr_name = scr_name.split('\\')[-1]
        count = 0
        print(f'Error! File named "{err_scr_name}.jpg" was not created! Please send this name to me!')

    time.sleep(random.uniform(0.5, 1.0))

    driver.find_element_by_xpath('/html/body').send_keys(Keys.RIGHT)

print('\nSuccess! All images are uploaded and saved to a folder.')

if zip_archive == 'Y':
    shutil.make_archive(path, 'zip', path)
    print('Success! Zip archive was created.\n')

driver.quit()
input('Click Enter to exit')
