import time

import requests
import csv


class Vk_group:

    def __init__(self, token):
        self.file_name = 'vk_group.csv'
        self.url = 'https://api.vk.com/method/wall.get?v=5.95&count=100'
        self.offset = 0
        self.token = token
        self.group_name = '&owner_id=-73519170'

    def __create_file(self):
        with open(self.file_name, newline='', mode='w', encoding='cp1251') as file_columns:
            file_writer = csv.writer(file_columns, delimiter='\t')
            file_writer.writerow(['Название', 'Описание', 'Фото'])

    def count_of_posts(self, url):
        r = requests.get(url)
        try:
            count_of_posts = r.json()['response']['count']
            return count_of_posts
        except KeyError as exc:
            print(exc, r.json())
            quit()

    def get_posts(self, json_):
        for posts in range(100):
            try:
                result_json = json_['response']['items']
                title = str(result_json[posts]['attachments'][0]['link']['title']).replace('\n', '').replace('\t', '')
                photo = result_json[posts]['attachments'][0]['link']['photo']['sizes'][-1]['url']
                description = str(result_json[posts]['text']).replace('\n', '').replace('\t', '')
                print(title, photo, description)
                with open('vk_group.csv', newline='', mode='a', encoding='cp1251') as file:
                    writer = csv.writer(file, delimiter='\t')
                    writer.writerow([title, description, photo])
            except KeyError:
                continue
            except IndexError:
                break

    def run(self):
        self.__create_file()
        for _ in range(8):
            need_url = self.url + '&offset=' + str(self.offset) + '&access_token=' + self.token + self.group_name
            r = requests.get(need_url)
            self.get_posts(json_=r.json())
            self.offset += 100


if __name__ == '__main__':
    pars = Vk_group(token='токен')
    pars.run()
