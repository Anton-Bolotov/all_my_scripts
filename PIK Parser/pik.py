import time
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.pik.ru/projects')
time.sleep(3)
soup_for_search_links = BeautifulSoup(driver.page_source, 'html.parser')
project_urls = soup_for_search_links.find_all('a', attrs={'target': '_self'})


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
try:
    for line in project_urls:
        if 'src=' in str(line):
            count += 1
            search_url = 'https://www.pik.ru/search' + line['href']
            date = BeautifulSoup(str(line), 'html.parser')
            project_name = date.find('h6').text
            project_mortgage = str(date).split('newPriceFormatTestB" type="micro">')[1].split('.</span></div>')[0]
            project_metro = str(date).split('Typography" type="subTitleTwo">')[1].split('</span></div><div class="')[0]
            project_walking_or_bus = str(date).split('Icons" id="" type="')[1].split('"><svg viewbox=')[0].replace('walkingMan', 'Пешком').replace('bus', 'Транспортом')
            project_time = str(date).split('Typography" type="micro">')[1].split('</span></div><div class="')[0]
            project_price = str(date).split('newPriceFormatTestA" type="micro">')[1].split('</span><span class="')[0]
            driver.set_window_size(300, 1080)
            driver.get(search_url)
            time.sleep(3)

            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            time.sleep(3)
            soup_for_rooms = BeautifulSoup(driver.page_source, 'html.parser')
            project_flats = soup_for_rooms.find_all('a', attrs={'target': '_blank'})

            for project_flat in project_flats:
                if 'Typography' in str(project_flat):
                    date_flat = BeautifulSoup(str(project_flat), 'html.parser')
                    # print(date_flat)
                    if 'type="lock"' in str(project_flat):
                        project_lock = 'Квартира забронирована'
                    else:
                        project_lock = 'Квартира свободная'

                    project_flat_url = 'https://www.pik.ru' + date_flat.find('a')['href']

                    project_location = str(date_flat).split('Typography" type="caption">')[1].split('</span></div><div class="')[0]

                    try:
                        project_body, project_section, project_floor = project_location.split(', ')
                    except ValueError:
                        project_body = project_section = project_floor = project_location

                    project_room_size = date_flat.find('h6').text
                    project_flat_type, project_flat_footage, *_ = project_room_size.split(' ')
                    project_settlement = str(date_flat).split('Typography" type="caption">')[2].split('</span>')[0]
                    project_finish = str(date_flat).split('Typography" type="micro">')[1].split('</span></span></div></div></div><div class="')[0]
                    project_full_price_1 = str(date_flat).split('type="subTitleOne">')[1].split('</span></div><div class="')[0]
                    project_price_per_month = str(date_flat).split('type="subTitleOne">')[2].split('</span></div><div class="')[0]
                    project_price_m2 = str(date_flat).split('Typography" type="micro">')[2].split('</span>')[0]
                    project_full_price_2 = str(date_flat).split('Typography" type="micro">')[3].split('</span>')[0]

                    with open(file=file_name, mode='a', encoding='utf-8') as file:
                        file.write(project_name + '\t' + project_metro + '\t' + project_walking_or_bus + '\t' + project_time
                                   + '\t' + project_price + '\t' + project_mortgage + '\t' + project_lock + '\t' + project_flat_url
                                   + '\t' + project_body + '\t' + project_section + '\t' + project_floor + '\t' + project_flat_type
                                   + '\t' + project_flat_footage + '\t' + project_settlement + '\t' + project_finish
                                   + '\t' + project_full_price_1 + '\t' + project_price_per_month + '\t' + project_price_m2
                                   + '\t' + project_full_price_2 + '\n')

            print(f'Пройдено {project_name} - {count} из 56')

except AttributeError:
    pass

driver.quit()
