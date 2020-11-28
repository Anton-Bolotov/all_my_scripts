import time
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys


some_dict = {}
with open(file='input.txt', mode='r', encoding='utf-8') as title_file:
    for title_ in title_file:
        title_name, title_link = title_.replace('\n', '').split('	')
        if title_name not in some_dict:
            some_dict.update({title_name: title_link})
        else:
            some_dict[title_name] += '\n' + title_link


driver = webdriver.Chrome()
driver.get('некий сайт')  # сайт с работы
driver.find_element_by_xpath('//*[@id="UserName"]').send_keys('логин')  # логин
driver.find_element_by_xpath('//*[@id="Password"]').send_keys('пароль')  # пароль
driver.find_element_by_xpath('//*[@id="loginForm"]/form/fieldset/input').click()

for title, links in some_dict.items():
    try:
        driver.find_element_by_xpath('//*[@id="search-box0"]').send_keys(title)
        driver.find_element_by_xpath('//*[@id="search-box0"]').click()
        driver.find_element_by_xpath('//*[@id="search-box0"]').send_keys(Keys.DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="search-box0"]').send_keys(Keys.DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="search-box0"]').send_keys(Keys.ENTER)
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        driver.find_element_by_xpath('//*[@id="main-menu"]/nav/ul/li[1]/a').click()
        continue
    driver.find_element_by_xpath('//*[@id="main-menu"]/nav/ul/li[7]/a').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="Text"]').send_keys(links)
    driver.find_element_by_xpath('//*[@id="body"]/div/form/input').click()
    driver.find_element_by_xpath('//*[@id="main-menu"]/nav/ul/li[1]/a').click()
driver.quit()
