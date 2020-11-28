import json
import requests
import urllib.parse
from list_of_file_extensions import white_list


link = 'https://cloud.mail.ru/public/39Bm/3EvnnJ5yL/'

good_links = set()
bad_links = []


def create_clear_date(urls):
    r = requests.get(urls)
    raw_data = r.text.split('window.cloudSettings =')[1].split(';</script>')[0]
    clear_data = raw_data.replace(r'\"*/:\x3c>?\\|', '').replace(r'\"*:\x3c>?\\|', '')
    return clear_data


def create_result_list(counts, date_to_loads_json):
    mail_json = json.loads(date_to_loads_json)
    try:
        result_list = mail_json['folders']['folder']['list'][counts]['weblink']
    except KeyError:
        result_list = mail_json['folders']['folder']['weblink']['error']
        print(result_list)
    return result_list


count = 0
break_count = 0
bad_links.append(link)

while True:

    if not bad_links:
        break_count += 1
    if break_count == 5:
        break

    for item in bad_links:
        print(bad_links)
        date = create_clear_date(urls=item)
        bad_links.remove(item)
        with open(file='output.txt', mode='w', encoding='utf-8') as file:
            for good_link in good_links:
                title_name = str(good_link).split('/')[6]
                url_encode = urllib.parse.quote(good_link)
                file.write(title_name + '\t' + str(url_encode.replace('%3A//', '://')) + '\n')
        with open(file='test_bad.txt', mode='w', encoding='utf-8') as ff:
            for bad_link in bad_links:
                ff.write(str(bad_link) + '\n')

        while True:
            try:
                result = create_result_list(counts=count, date_to_loads_json=date)
                if result == 'not_exists':
                    break
                check_result = str(result).split('.')[-1]
                if check_result in white_list:
                    good_links.add('https://cloud.mail.ru/public/' + str(result))
                else:
                    if 'https://cloud.mail.ru/public/' + str(result) not in bad_links:
                        bad_links.append('https://cloud.mail.ru/public/' + str(result))
                count += 1
            except IndexError:
                count = 0
                break


# for items in good_links:
#     print(items)
#
# for bad_items in bad_links:
#     print(bad_items.split('.')[-1])
