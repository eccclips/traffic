from telethon import TelegramClient, sync

# Введите свои API ID и API Hash
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# Создайте объект клиента
client = TelegramClient('session_name', api_id, api_hash)

# Войдите в систему
client.start()

# Укажите канал, который хотите парсить
channel_username = 'channel_username'

# Получите последние 100 сообщений из канала
messages = client.get_messages(channel_username, limit=100)

# Выведите содержимое сообщений
for message in messages:
    print(message.sender_id, message.text)

# Закройте сессию клиента
client.disconnect()