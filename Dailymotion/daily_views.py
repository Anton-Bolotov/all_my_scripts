import requests

with open(file='input.txt', mode='r', encoding='utf-8') as file:
    for url in file:
        url = url.replace('\n', '')
        id_video = url.split('/video/')[1]
        try:
            r = requests.get(f'https://api.dailymotion.com/video/{id_video}?fields=views_total,duration')
            views = str(r.json()['views_total'])
            duration = str(r.json()['duration'] // 60) + ':' + str(r.json()['duration'] % 60) + ' min'
        except KeyError:
            views = 'Удалено'
            duration = 'Удалено'
        print(url + '\t' + views + '\t' + duration)
