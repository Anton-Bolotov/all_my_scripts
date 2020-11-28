import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

count = 0
title_count = 0
count_rem = 1
title_list = []
with open(file='input.txt', mode='r', encoding='utf-8') as title_file:
    for title_ in title_file:
        title_ = title_.replace('\n', '')
        title_list.append(title_)


driver = webdriver.Chrome()
driver.get('некий сайт')  # сайт с работы
driver.find_element_by_xpath('//*[@id="UserName"]').send_keys('логин')  # логин
driver.find_element_by_xpath('//*[@id="Password"]').send_keys('пароль')  # пароль
driver.find_element_by_xpath('//*[@id="loginForm"]/form/fieldset/input').click()

for title in title_list:
    title_count += 1
    driver.find_element_by_xpath('//*[@id="search-box0"]').send_keys(title)
    driver.find_element_by_xpath('//*[@id="search-box0"]').click()
    driver.find_element_by_xpath('//*[@id="search-box0"]').send_keys(Keys.DOWN)
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="search-box0"]').send_keys(Keys.DOWN)
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="search-box0"]').send_keys(Keys.ENTER)
    driver.switch_to.alert.accept()

    while True:
        if 'more pages' in str(driver.page_source):
            time.sleep(0.2)
            try:
                driver.find_element_by_xpath(f'//*[@id="recheck-requests-mount-point"]/div/div[{count_rem}]/a').click()
                driver.find_element_by_xpath(f'//*[@id="recheck-requests-mount-point"]/div/div[{count_rem}]/span/a[2]').click()
                driver.find_element_by_xpath('//*[@id="body"]/div/ul/li[6]/a').click()
                count_rem = 1
            except NoSuchElementException:
                count_rem += 1
        else:
            count += 1
            try:
                time.sleep(0.1)
                driver.find_element_by_xpath(
                    f'//*[@id="recheck-requests-mount-point"]/div/div[{count}]/ul/li/span[2]/a[2]').click()
            except ElementNotInteractableException:
                continue
            except NoSuchElementException:
                driver.find_element_by_xpath('//*[@id="body"]/div/ul/li[6]/a').click()
                count = 0
                if 'Removed' not in str(driver.page_source):
                    driver.find_element_by_xpath('//*[@id="main-menu"]/nav/ul/li[1]/a').click()
                    print(f'Речек тайтла - {title} чист! (пройдено - {title_count} из {len(title_list)})')
                    break
driver.quit()
