import requests
import json
import time

API_KEY = 'Ваш API ключ'


def get_json(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data


def make_api_link(url, part):
    video_id = url.split('=')[1]
    return 'https://www.googleapis.com/youtube/v3/videos?part=' + part + '&id=' + video_id + '&key=' + API_KEY


def get_views(url):
    json_data = get_json(make_api_link(url, 'statistics'))
    return json_data['items'][0]['statistics']['viewCount']


def get_name(url):
    json_data = get_json(make_api_link(url, 'snippet'))
    return json_data['items'][0]['snippet']['title']


def get_date(url):
    json_data = get_json(make_api_link(url, 'snippet'))
    return json_data['items'][0]['snippet']['publishedAt']


def get_channel_ID(url):
    json_data = get_json(make_api_link(url, 'snippet'))
    return json_data['items'][0]['snippet']['channelId']


def get_duration(url):
    json_data = get_json(make_api_link(url, part='contentDetails'))
    return json_data['items'][0]['contentDetails']['duration']


def check_channel(channelID, part):
    api_link = 'https://www.googleapis.com/youtube/v3/channels?part=' + part + '&id=' + channelID + '&key=' + API_KEY
    json_data = get_json(api_link)
    return json_data


def counting():
    count = 0
    with open(file='input.txt', mode='r', encoding='utf-8')as file:
        for _ in file:
            count += 1
    return count


def test_json(url):
    snippet = 'contentDetails'
    tets_data = get_json(make_api_link(url, snippet))
    return tets_data


def make_all(url):
    try:
        views = get_views(url)
        name = get_name(url)
        date = get_date(url)
        ch_id = get_channel_ID(url)
        duration = str(get_duration(url)).replace('PT', '')
        channel_link = "https://www.youtube.com/channel/" + ch_id
        print(str(url) + '\t' + str(views) + '\t' + str(name) + '\t' + str(date.split('T')[0])
                       + '\t' + str(channel_link) + '\t' + duration)
        with open(file='output.txt', mode='a', encoding='utf-8') as file:
            file.write(str(url) + '\t' + str(views) + '\t' + str(name) + '\t' + str(date.split('T')[0])
                       + '\t' + str(channel_link) + '\t' + duration + '\n')
    except KeyError:
        print(f'{url}\tКончилась квота - \t{test_json(url)}')
    except IndexError:
        print(f'Ссылка мертва\t{url}')


def main():
    count = 0
    with open(file='output.txt', mode='w', encoding='utf-8') as file:
        file.write('Links' + '\t' + 'Views' + '\t' + 'Name' + '\t' + 'Date upload' + '\t' + 'Channel' + '\t' + 'duration' + '\n')
    file = open('input.txt', 'r')
    urls = [url.strip() for url in file]
    file.close()

    for url in urls:
        count += 1
        # print(f'ссылка -\t{url}\tпройдено ссылок {count} из {counting()}')
        make_all(url)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
