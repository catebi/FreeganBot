from dotenv import load_dotenv
import os
import logging
import yaml
import re
from telethon import TelegramClient, events, errors

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

logging.warning('bot started...')

env = os.getenv('ENV', 'dev')  # Default to 'prod' if ENV is not set
config_file_name = 'config.dev.yaml' if env == 'dev' else 'config.yaml'

# Now, use os.getenv to read the environment variables
api_id = int(os.getenv('TELEGRAM_API_ID', 0))
api_hash = str(os.getenv('TELEGRAM_API_HASH'))

# TODO: not used yet, investigate
# bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

chat_send_to = str(os.getenv('TELEGRAM_CHAT_SEND_TO'))

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
            # logging.warning(f"Keyword '{word}' found in chat {event.chat.username}: {event.text}")
            message = f"{event.text}\n\n[t.me/{event.chat.username}/{event.id}](t.me/{event.chat.username}/{event.id})"
            await client.send_message(chat_send_to, message, file=event.photo)
            break

def main():
    # client.start(bot_token=bot_token)
    logging.warning('[main]started..')
    try:
        client.start()
        logging.warning("Client is connected.")
        # Your code here
    except errors.PhoneNumberInvalidError:
        logging.error("Error: The phone number is invalid")
    except errors.AuthKeyError:
        logging.error("Error: The authorization key is invalid")
    except errors.TimedOutError:
        logging.error("Error: Failed to connect to Telegram servers by timeout")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    logging.warning("Client started. Listening for messages...")
    client.run_until_disconnected()

main()