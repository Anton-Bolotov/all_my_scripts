import time
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.pik.ru/projects')
time.sleep(2)
soup_for_search_links = BeautifulSoup(driver.page_source, 'html.parser')
project_urls = soup_for_search_links.find_all('a', attrs={'class': 'styles__Project-sc-15y9oll-1 hnKNUU'})

SCROLL_PAUSE_TIME = 3
now = datetime.datetime.now()
file_name_date = now.strftime('%d-%m-%Y_%H-%M')

file_name = f'result_{file_name_date}.txt'

with open(file=file_name, mode='w', encoding='utf-8') as file:
    file.write('Название ЖК\t' + 'Станция метро\t' + 'Пешком или транспортом\t' + 'Время до метро\t'
               + 'Минимальная цена\t' + 'Минимальная выплата по ипотеке\t' + 'Статус квартиры\t'
               + 'Ссылка на квартиру\t' + 'Корпус\t' + 'Секция\t' + 'Этаж\t' + 'Тип квартиры\t' + 'м²\t'
               + 'Заселение\t' + 'Отделка\t' + 'Полная цена\t' + 'Примерный ипотечный платеж\t'
               + 'Цена за м²\t' + 'Полная цена 2\n')
count = 0
for line in project_urls:
    count += 1
    search_url = 'https://www.pik.ru/search' + line['href']
    date = BeautifulSoup(str(line), 'html.parser')

    project_name = date.find('h6', attrs={'class': 'sc-bdVaJa hPmloc Typography'}).text
    project_metro = date.find('span', attrs={'class': 'sc-bdVaJa jmcaIA Typography'}).text
    project_walking_or_bus = date.find('div', attrs={'class': 'sc-ifAKCX gWhHCO Icons'})['type'].replace('walkingMan',
                                                                                                         'Пешком').replace(
        'bus', 'Транспортом')
    project_time = date.find('span', attrs={'class': 'sc-bdVaJa bFHpWm Typography'}).text
    project_price = date.find('span', attrs={'class': 'sc-bdVaJa dNFKvG Typography newPriceFormatTestA'}).text
    project_mortgage = date.find('span', attrs={'class': 'sc-bdVaJa dNFKvG Typography newPriceFormatTestB'}).text

    driver.get(search_url)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup_for_rooms = BeautifulSoup(driver.page_source, 'html.parser')
    project_flats = soup_for_rooms.find_all('div', attrs={'class': 'sc-dEfkYy jRtlGa'})

    for project_flat in project_flats:
        date_flat = BeautifulSoup(str(project_flat), 'html.parser')

        if 'type="lock"' in str(project_flat):
            project_lock = 'Квартира забронирована'
        else:
            project_lock = 'Квартира свободная'

        project_flat_url = 'https://www.pik.ru' + date_flat.find('a', attrs={'class': 'sc-cqPOvA jnHgMU'})['href']
        project_location = date_flat.find('div', attrs={'class': 'sc-fjhmcy ifEfmX'}).text

        try:
            project_body, project_section, project_floor = project_location.split(', ')
        except ValueError:
            project_body = project_section = project_floor = project_location

        project_room_size = date_flat.find('div', attrs={'class': 'sc-iuDHTM bKufRk'}).text
        project_flat_type, project_flat_footage, *_ = project_room_size.split(' ')
        project_settlement = date_flat.find('div', attrs={'class': 'sc-erNlkL bSiriq'}).text
        project_finish = date_flat.find('div', attrs={'class': 'sc-kEmuub kYCymK'}).text
        project_full_price_1 = date_flat.find('div', attrs={'class': 'sc-dznXNo hKrVhA newPriceFormatTestA'}).text
        project_price_per_month = date_flat.find('div', attrs={'class': 'sc-dznXNo hKrVhA newPriceFormatTestB'}).text
        project_price_m2 = date_flat.find('div', attrs={'class': 'sc-bbkauy jVNgZy newPriceFormatTestA'}).text
        project_full_price_2 = date_flat.find('div', attrs={'class': 'sc-bbkauy jVNgZy newPriceFormatTestB'}).text

        with open(file=file_name, mode='a', encoding='utf-8') as file:
            file.write(project_name + '\t' + project_metro + '\t' + project_walking_or_bus + '\t' + project_time
                       + '\t' + project_price + '\t' + project_mortgage + '\t' + project_lock + '\t' + project_flat_url
                       + '\t' + project_body + '\t' + project_section + '\t' + project_floor + '\t' + project_flat_type
                       + '\t' + project_flat_footage + '\t' + project_settlement + '\t' + project_finish
                       + '\t' + project_full_price_1 + '\t' + project_price_per_month + '\t' + project_price_m2
                       + '\t' + project_full_price_2 + '\n')

    print(f'Пройдено {project_name} - {count} из 56')

driver.quit()
