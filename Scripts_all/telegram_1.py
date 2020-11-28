import requests
from bs4 import BeautifulSoup

with open(file='input.txt', mode='r', encoding='utf-8') as file:
    for url in file:
        url = url.replace('\n', '')
        tg_url = url + '?embed=1'
        r = requests.get(tg_url)
        soup = BeautifulSoup(r.text, "html.parser")
        if 'not found' in str(soup):
            views = 'Channel not found'
        else:
            try:
                views = soup.find("span", {"class": "tgme_widget_message_views"}).text
            except AttributeError:
                views = '0'
        print(url + '\t' + views)

