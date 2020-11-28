import requests
import re
import time


def count_of_links(file_in):
    _count = 0
    with open(file=file_in, mode='r', encoding='utf-8') as links_file:
        for _ in links_file:
            _count += 1
    return _count


def run(vk_group, token, full_name_of_group):
    group_ids = '&group_ids=' + vk_group
    fields = '&fields=members_count,status,description,activity,deactivated'

    api_get = 'https://api.vk.com/method/groups.getById?v=5.95' + fields + '&' + token + group_ids

    r = requests.get(api_get)
    json = r.json()
    try:
        json_vk = json['response'][0]
        try:
            with open(file='output.txt', mode='a', encoding='utf-8') as file_write:
                file_write.write(
                    str(full_name_of_group) + '\t' +
                    str(json_vk["deactivated"]) + '\n'
                )
        except KeyError:
            with open(file='output.txt', mode='a', encoding='utf-8') as file_write:
                file_write.write(
                    str(full_name_of_group).replace('\n', '').replace('\t', '') + '\t' +
                    'active' + '\t' +
                    str(json_vk["members_count"]).replace('\n', '').replace('\t', '') + '\t' +
                    str(json_vk["status"]).replace('\n', '').replace('\t', '') + '\t' +
                    str(json_vk["description"]).replace('\n', '').replace('\t', '') + '\t' +
                    str(json_vk["activity"]).replace('\n', '').replace('\t', '') + '\n'
                )
    except KeyError:
        with open(file='output.txt', mode='a', encoding='utf-8') as file_write:
            file_write.write(
                str(full_name_of_group) + '\t' +
                'not sure' + '\n'
            )


REGULAR = r'public\d{6,}'
access_token = 'access_token=21321321'  # Ваш токен

with open(file='output.txt', mode='w', encoding='utf-8') as file_header:
    file_header.write(
        'Группа' + '\t' +
        'Статус' + '\t' +
        'Количество пользователей' + '\t' +
        'Статус группы' + '\t' +
        'Описание группы' + '\t' +
        'Направленность группы' + '\n'
    )

count = 0
need_count = count_of_links('input.txt')
start_time = time.time()
with open(file='input.txt', mode='r', encoding='utf-8') as file:
    for vk_links in file:
        time.sleep(0.2)
        count += 1
        vk_links = vk_links.replace('\n', '')
        group_vk = vk_links.split('/')[3]
        match = re.search(REGULAR, group_vk)
        if match:
            url_pub = match.group().replace('public', '')
            run(vk_group=url_pub, token=access_token, full_name_of_group=vk_links)
        else:
            run(vk_group=group_vk, token=access_token, full_name_of_group=vk_links)

        end_time = time.time()
        print(f'Пройдено ссылок - {count}  из {need_count}, '
              f'времени прошло с начала проверки - {round(end_time - start_time, 2)} секунд')

input('\nДля выхода из программы нажмите Enter')
