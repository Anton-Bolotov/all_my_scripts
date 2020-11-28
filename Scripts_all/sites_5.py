import requests
from bs4 import BeautifulSoup


with open(file='output.txt', mode='w', encoding='utf-8') as ff:
    ff.write('Ссылка' + '\t' + 'Название' + '\n')

with open(file='input.txt', mode='r', encoding='utf-8') as file:
    for url in file:
        url = url.replace('\n', '')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        if '://dropapk' in url:
            try:
                title_name = soup.find('h1', attrs={'class': 'title mb-2'}).text
            except:
                title_name = 'Что-то пошло не так'
            with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                ff.write(str(url) + '\t' + str(title_name) + '\n')
            print(url + '\t' + str(title_name))
        elif '://monova' in url:
            try:
                title_name = str(soup.find('title').text).replace(' - Torrent', '')
            except:
                title_name = 'Что-то пошло не так'
            with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                ff.write(str(url) + '\t' + str(title_name) + '\n')
            print(url + '\t' + title_name)
        elif '://torrentz2' in url:
            try:
                title_name = str(soup.find('title').text).replace(' Download', '')
            except:
                title_name = 'Что-то пошло не так'
            with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                ff.write(str(url) + '\t' + str(title_name) + '\n')
            print(url + '\t' + title_name)
        elif '://uptobox' in url:
            try:
                title_name = soup.find('h1', attrs={'class', 'file-title'}).text
            except:
                title_name = 'Что-то пошло не так'
            with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                ff.write(str(url) + '\t' + str(title_name) + '\n')
            print(url + '\t' + str(title_name))
        elif '.zippyshare' in url:
            try:
                title_name = str(soup.find('title').text).replace('Zippyshare.com - ', '')
            except:
                title_name = 'Что-то пошло не так'
            with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                ff.write(str(url) + '\t' + str(title_name) + '\n')
            print(url + '\t' + str(title_name))
