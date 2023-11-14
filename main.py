from dotenv import load_dotenv
import os
from telethon import TelegramClient, events

# Load environment variables from .env file
load_dotenv()

# Now, use os.getenv to read the environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
chatFrom = os.getenv('TELEGRAM_CHAT_FROM')
chat = os.getenv('TELEGRAM_CHAT')

# ... rest of your script ...
client = TelegramClient('anon', api_id, api_hash)
client.start()
key_words = ["Кошачий", "кошачий", "Клетка", "клетка", 'Вольер', 'вольер']

@client.on(events.NewMessage(chats=(chatFrom,)))
async def main(event):
    channel = await client.get_entity(event.chat_id)
    for word in key_words:
        if word in event.text:
            await client.send_message(chat, event.text + "\n" + "t.me/" + str(channel.username) + "/" + str(event.id), file=event.photo)
            print(word)
            break

client.run_until_disconnected()