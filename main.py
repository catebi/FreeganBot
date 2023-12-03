from dotenv import load_dotenv
import os
import logging
import yaml
import re
from telethon import TelegramClient, events

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env = os.getenv('ENV', 'dev')  # Default to 'prod' if ENV is not set
config_file_name = 'config.dev.yaml' if env == 'dev' else 'config.yaml'

# Now, use os.getenv to read the environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

# TODO: not used yet, investigate
# bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

chat_send_to = os.getenv('TELEGRAM_CHAT_SEND_TO')

# Load the configuration from the YAML file
with open(config_file_name, encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

# Extract chat URLs and keywords from the config
chat_urls = config['chats']
keywords = config['keywords']

# Initialize the client
client = TelegramClient('catebi_freegan', api_id, api_hash)

@client.on(events.NewMessage(chats=chat_urls))
async def new_message_listener(event):
    for word in keywords:
        text = event.text.lower()
        if re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(text):
            print(f"Keyword '{word}' found in chat {event.chat.username}: {event.text}")
            await client.send_message(chat_send_to, event.text + "\n" + "t.me/" + str(event.chat.username) + "/" + str(event.id), file=event.photo)
            break

async def main():
    # await client .start(bot_token=bot_token)
    await client.start()
    print("Client started. Listening for messages...")
    await client.run_until_disconnected()

import asyncio
asyncio.run(main())