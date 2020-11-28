from telethon import TelegramClient
import configparser

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
user_name = config['Telegram']['username']

# Сюда вводить каналы телеграма
telegram_channel = [
    'https://t.me/tree_gamers/',
]

search_request = 'Call Of Duty' # Сюда вводить поисковый запрос


class Telegram:

    def __init__(self, _channel, _search, _api_id, _api_hash):
        self.channel = _channel
        self.search = _search
        self.id = _api_id
        self.hash = _api_hash

    def telegram(self):
        try:
            for message in client.iter_messages(self.channel, search=self.search):
                print(self.channel + str(message.id) + '\t' + str(message.text).replace('\n', ''))
        except:
            print(self.channel)


client = TelegramClient(user_name, api_id, api_hash)
client.start()
for channel in telegram_channel:
    telegram = Telegram(_channel=channel, _search=search_request, _api_id=api_id, _api_hash=api_hash)
    telegram.telegram()

