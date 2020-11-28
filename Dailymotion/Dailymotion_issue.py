import csv
import time
from datetime import datetime
import requests


class Dailymotion:

    def __init__(self, search_query):
        self.api_daily = 'https://api.dailymotion.com/videos?limit=100'
        self.fields = '&fields=id,title,description,views_total,user.username,duration,created_time&search='
        self.search_query = str(search_query)
        self.count_page = 0
        self.file_name = 'dailymotion_result.csv'

    def write_csv_file(self, list_to_write):
        try:
            with open(self.file_name, newline='', mode='a') as file:
                writer = csv.writer(file, delimiter='\t', )
                writer.writerow(list_to_write)
        except UnicodeEncodeError:
            with open(self.file_name, newline='', mode='a', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(list_to_write)

    def run(self):
        try:
            while True:
                self.count_page += 1
                url = self.api_daily + self.fields + self.search_query + '&page=' + str(self.count_page)
                r = requests.get(url)
                daily_json = r.json()['list']
                if r.json()['page'] == 11:
                    break
                for items in daily_json:
                    link = 'https://www.dailymotion.com/video/' + items['id']
                    title = str(items['title']).replace(';', '')
                    description = str(items['description']).replace('\n', '').replace('\t', '').replace(';', '')
                    views = items['views_total']
                    user_name = items['user.username']
                    duration = str(items['duration'] // 60) + ':' + str(items['duration'] % 60) + ' min'
                    date_uploaded = datetime.utcfromtimestamp(items['created_time']).strftime('%d-%m-%Y %H:%M:%S')
                    list_with_columns = [
                        link, self.search_query, title, views, duration, user_name, date_uploaded, description
                    ]
                    self.write_csv_file(list_with_columns)
        except KeyError:
            print(f'---> Был введен пустой запрос, он не был обработан!')


if __name__ == '__main__':
    input_list = []
    print('---> Грабер выдачи Dailymotion.com v.0.2.1.0')
    print('---> Если необходимо ввести несколько запросов - введите запрос и нажмите Enter')

    with open('dailymotion_result.csv', newline='', mode='w') as file_columns:
        file_writer = csv.writer(file_columns, delimiter='\t')
        file_writer.writerow(['Ссылка', 'Введенный запрос', 'Название видео', 'Просмотры', 'Длительность видео',
                              'Пользователь загрузивший видео', 'Дата загрузки видео', 'Описание'])

    while True:
        search_input = input('---> Введите запрос для поиска - ')
        input_list.append(search_input)
        check_input = input('---> Желаете ввести еще 1 запрос ? y/n - ')
        if check_input != 'y':
            break

    print('---> Начало сбора данных')
    start_time = time.time()
    for q_search in input_list:
        daily = Dailymotion(search_query=q_search)
        daily.run()
    end_time = time.time()
    print(f'---> Времени затраченно на прохождение - {len(input_list)} запросов ({round(end_time - start_time)} секунд)')
    input('---> Для выхода из программы нажмите Enter')
