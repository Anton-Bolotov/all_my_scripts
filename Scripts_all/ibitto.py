import requests
from bs4 import BeautifulSoup

proxies = {'https': '95.174.67.50:18080'}

with open(file='input.txt', mode='r', encoding='utf-8') as file:
    for url in file:
        url = url.replace('\n', '')
        try:
            r = requests.get(url, proxies=proxies)
            soup = BeautifulSoup(r.text, 'html.parser')
            if 'The torrent has been deleted for one of these reasons' in str(soup):
                print(url + '\t' + 'Удалено')
            else:
                print(url + '\t' + 'Живо')
        except OSError:
            print(url + '\t' + 'Перепроверить')
