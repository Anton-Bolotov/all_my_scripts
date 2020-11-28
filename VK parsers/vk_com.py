import time
import requests
from bs4 import BeautifulSoup

import vk_api
vk_session = vk_api.VkApi(token='Ваш токен')
vk = vk_session.get_api()

with open(file='input.txt', mode='r', encoding='utf-8') as file:
    for url in file:
        time.sleep(0.2)
        url = url.replace('\n', '')
        if 'vk.com' in url:
            try:
                vk_url = url.split('vk.com/video')[1]
                views = vk.video.get(videos=vk_url)['items'][0]['views']
            except IndexError:
                views = 'Посты не могу обработать'
            print(str(url) + '\t' + str(views))

        elif 'ok.ru' in url:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            vnf = soup.find('span', attrs={'class': 'vp-layer-info_i vp-layer-info_views'}).text
            views = vnf.replace(' ', '').split('прос')[0]
            print(str(url) + '\t' + str(views))
