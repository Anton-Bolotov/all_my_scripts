import requests
import csv

url = 'https://api.vk.com/method/wall.get?v=5.95&count=100'
offset = 0
token = '&access_token=b33bf24f680a638f09ff04164b'
grop_name = '&owner_id=-73519170'


while True:
    try:
        need_url = url + '&offset=' + str(offset) + token + grop_name
        r = requests.get(need_url)
        count_of_posts = r.json()['response']['count']
        result_json = r.json()['response']['items']
        for post in range(count_of_posts):
            try:
                title = str(result_json[post]['attachments'][0]['link']['title']).replace('\n', '').replace('\t', '')
                photo = result_json[post]['attachments'][0]['link']['photo']['sizes'][-1]['url']
                description = str(result_json[post]['text']).replace('\n', '').replace('\t', '')
                with open(file='output.txt', mode='a', encoding='utf-8') as ff:
                    ff.write(title + '\t' + description + '\t' + photo + '\n')
            except KeyError:
                continue
    except IndexError:
        offset += 100
    except KeyError as exc:
        if exc == 'response':
            break
