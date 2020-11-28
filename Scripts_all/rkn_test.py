import requests
from bs4 import BeautifulSoup
import json
import threading

some_set = set()
count = 0
url = 'https://cloud.mail.ru/public/2FLE/2nwS2sz3d/%5Bslivysklad.com%5D%20%5BSkillbox%5D%20%D0%A1%D0%BA%D0%B2%D0%BE%D0%B7%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0%20(2019)/%5Bslivysklad.com%5D%20mp3/'

# class Cloud_mail(threading.Thread):
#
#     def __init__(self, link):
#         super().__init__()
#         self.link = link
#         self.count = 0
#         self.set_for_url = set()
#
#     def create_json(self):
#         r = requests.get(self.link)
#         soup = BeautifulSoup(r.text, 'lxml')
#         site_mail = str(soup.findAll('script')[-9]).replace('<script>window.cloudSettings =', '').replace(
#             ';</script>', '').replace(r'\\n', '').replace(r'"\"*/:\x3c>?\\|"', '"lol"').replace(r'"\"*:\x3c>?\\|"',
#                                                                                                 '"lol"')
#         json_ = json.loads(site_mail)
#         return json_
#
#     def main(self):
#         json_with_content = self.create_json()
#         folder_with_content = json_with_content['folders']['tree'][0]['list'][0]['items']
#         for urls in folder_with_content:
#             urls = 'https://cloud.mail.ru/public/' + str(urls)
#             self.set_for_url.add(urls)
#
#     def pod_main(self):
#         json_with_content = self.create_json()
#         try:
#             for _ in range(30):
#                 folder_with_content = json_with_content['folders']['tree'][1]['list'][self.count]['items']
#                 print(folder_with_content)
#                 self.count += 1
#                 if folder_with_content:
#                     for items in folder_with_content:
#                         self.set_for_url.add(items)
#         except IndexError:
#             self.count = 0
#
#
# mail = Cloud_mail(link=url)
# mail.pod_main()
# print(mail.set_for_url)

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
site_mail = str(soup.findAll('script')[-9]).replace('<script>window.cloudSettings =', '').replace(
    ';</script>', '').replace(r'\\n', '').replace(r'"\"*/:\x3c>?\\|"', '"lol"').replace(r'"\"*:\x3c>?\\|"',
                                                                                        '"lol"')
json_ = json.loads(site_mail)
count2 = 0
try:
    for _ in range(25):
        folder_with_content = json_['folders']['tree'][count2]['list'][count]['items']
        count2 += 1
        for _ in range(25):
            count += 1
            if folder_with_content:
                for items in folder_with_content:
                    print('https://cloud.mail.ru/public/' + str(items))
except IndexError:
    count = 0
    count2 = 0

