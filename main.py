from dotenv import load_dotenv
import os
import logging
from telethon import TelegramClient, events

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Now, use os.getenv to read the environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
chatFrom = os.getenv('TELEGRAM_CHAT_FROM')
chat = os.getenv('TELEGRAM_CHAT')

# ... rest of your script ...
client = TelegramClient('anon', api_id, api_hash)
client.start()
key_words = ["кошачий", "клетка", 'вольер']

@client.on(events.NewMessage(chats=(chatFrom,)))
async def main(event):
    # Log the incoming message
    # logging.info(f"New message in chat {event.chat_id}: {event.text}")

    channel = await client.get_entity(event.chat_id)
    for word in key_words:
        if word in event.text.lower():
            await client.send_message(chat, event.text + "\n" + "t.me/" + str(channel.username) + "/" + str(event.id), file=event.photo)
            break

client.run_until_disconnected()
