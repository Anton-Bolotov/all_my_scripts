import time
import requests
import threading
from bs4 import BeautifulSoup
import csv


class Parsing(threading.Thread):

    def __init__(self, name, url):
        super().__init__()
        self.name = name
        self.url = url

    def run(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        source = str(soup.find_all('div', attrs={'class': 'sp-video__item-page-new__video-content video'}))
        result = BeautifulSoup(source, 'html.parser')

        title = result.find('h1', attrs={'class': 'sp-video__item-page-new__title'}).text
        channel_name = result.find('a', attrs={'class': 'sp-video__item-page-new__info__author-name js-router-link'}).text
        _channel = str(result.find('a', attrs={'class': 'sp-video__item-page-new__info__author-name js-router-link'})).split('href="')[1].split('">')[0]
        channel_url = 'https://my.mail.ru' + _channel

        try:
            views = result.find('span', attrs={'class': 'sp-video__item-page-new__info__views'}).text.replace('\n', '').replace('\t', '')
        except AttributeError:
            views = '0'

        upload_date = result.find('time', attrs={'class': 'sp-video__item-page-new__info__date'}).text
        duration = str(result.find('meta', attrs={'itemprop': 'duration'})).split('content="')[1].split('" ')[0].replace('PT', '')

        likes, _, comments = result.find_all('meta', attrs={'itemprop': 'interactionCount'})
        likes = str(likes).split('content="')[1].split('" ')[0].replace('UserLikes:', '')
        comments = str(comments).split('content="')[1].split('" ')[0].replace('UserComments:', '')
        list_to_write = [self.url, title, channel_name, channel_url, views, upload_date, duration, likes, comments]

        try:
            with open(file='../mail_ru_result.csv', newline='', mode='a') as ff:
                writer = csv.writer(ff, delimiter='\t', )
                writer.writerow(list_to_write)
        except UnicodeEncodeError:
            with open(file='../mail_ru_result.csv', newline='', mode='a', encoding='utf-8') as ff:
                writer = csv.writer(ff, delimiter='\t', )
                writer.writerow(list_to_write)


start_time = time.time()
threads = []
count = 0
with open('../mail_ru_result.csv', newline='', mode='w') as file_columns:
    file_writer = csv.writer(file_columns, delimiter='\t')
    file_writer.writerow(['Ссылка', 'Название', 'Название Канала', 'Ссылка на Канал', 'Просмотры',
                          'Дата Загрузки', 'Длительность', 'Кол-во Лайков', 'Кол-во Комментариев'])


with open(file='../input.txt', mode='r', encoding='utf-8') as file:
    for urls in file:
        urls = urls.replace('\n', '')
        if '.html' in urls:
            count += 1
            pars = Parsing(name=str(count), url=urls)
            pars.start()
            threads.append(pars)
            if threading.active_count() >= 400:
                for t in threads:
                    t.join()
for t in threads:
    t.join()
end_time = time.time()

print(f'Время затраченное на обработку {count} ссылок mail.ru - ', round(end_time - start_time, 2), 'секунд')
print('Результат выполнения смотри в файле - mail_ru_result.csv')
input('Для выхода из программы нажмите Enter')
