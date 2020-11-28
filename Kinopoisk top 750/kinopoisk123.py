import json
import time
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.1.8) Gecko/20100214 Linux Mint/8 (Helena) Firefox/'
                  '3.5.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
    'Accept-Encoding': 'deflate',
    'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '300',
    'Connection': 'keep-alive',
    'Referer': 'http://www.kinopoisk.ru/',
    'Cookie': 'users_info[check_sh_bool]=none; search_last_date=2010-02-19; search_last_month=2010-02;'
              '                                        PHPSESSID=b6df76a958983da150476d9cfa0aab18',
}
count = 0
with open(file='input.txt', mode='r', encoding='utf-8') as file:
    for url in file:
        count += 1
        url = url.replace('\n', '')
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        json_knp = str(soup.find('script', attrs={'id': '__NEXT_DATA__'})).split('type="application/json">')[1].replace('</script>', '')
        id_film = url.split('/')[4]
        director_id_key = '$Film:' + str(id_film) + '.members({"limit":4,"role":"DIRECTOR"}).items.0'
        person_id = json.loads(json_knp)['props']['apolloState']['data'][director_id_key]['person']['id']
        try:
            original_name = json.loads(json_knp)['props']['apolloState']['data'][person_id]['name']
            if original_name is None:
                raise KeyError
        except KeyError:
            original_name = json.loads(json_knp)['props']['apolloState']['data'][person_id]['originalName']
        print(str(count) + '\t' + url + '\t' + original_name)
