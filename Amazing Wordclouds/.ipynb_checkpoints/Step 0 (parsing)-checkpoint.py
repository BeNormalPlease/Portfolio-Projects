import configparser
import json
from telethon.sync import TelegramClient
from datetime import date, datetime
from telethon.tl.functions.messages import GetHistoryRequest

# Считываем учетные данные для доступа к telethon
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

client.start()


# Сама функция для парсинга
async def dump_all_messages(channel):
    offset_msg = 0
    limit_msg = 100  # максимальное число записей, передаваемых за один раз, чтобы ничего не сломалось
    all_messages = []
    total_messages = 0
    total_count_limit = 10000  # Лимит постов 10000, т.к в 'Риа Новости' и 'Рифмы и Панчи' постов > 50к, а в других 2 каналах чуть меньше 10к

    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open('outfile.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
    url = input("Введите ссылку на канал или чат: ")
    channel = await client.get_entity(url)
    await dump_all_messages(channel)
# Поэтапно ввёл все 4 интересующих меня канала и результат можно увидеть в папке 'Step 0'


with client:
    client.loop.run_until_complete(main())
