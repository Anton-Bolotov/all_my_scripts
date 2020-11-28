import time

import requests
import threading
from bs4 import BeautifulSoup


class Parsing(threading.Thread):

    def __init__(self, name, url):
        super().__init__()
        self.name = name
        self.url = url

    def run(self):
        try:
            r = requests.get(self.url)
            soup = BeautifulSoup(r.text, "html.parser")
            if 'Ошибка обработки видео' not in str(soup):
                a = soup.findAll('span', attrs={'class': 'ctview'})[0]
                # print(self.name + '\t' + self.url + '\t' + str(a).split('>')[1].split('<')[0] + '\n', flush=True)
                with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                    ff.write(self.name + '\t' + self.url + '\t' + str(a).split('>')[1].split('<')[0] + '\n')
            else:
                print('Ошибка обработки видео' + '\t' + self.url)
        except:
            print('Эту ссылку придется перепроверить' + '\t' + self.url)


start_time = time.time()
threads = []
count = 0
with open(file='output.txt', mode='w', encoding='utf-8') as ff:
    ff.write('Номер' + '\t' + 'Ссылка' + '\t' + 'Просмотры' + '\n')
with open(file='input.txt', mode='r', encoding='utf-8') as file:
    for urls in file:
        count += 1
        urls = urls.replace('\n', '')
        pars = Parsing(name=str(count), url=urls)
        pars.start()
        threads.append(pars)
        if threading.active_count() >= 400:
            for t in threads:
                t.join()
for t in threads:
    t.join()
end_time = time.time()
print(f'Время на обработку {count} ссылок сибнета - ', round(end_time - start_time, 2), 'секунд')
