from dotenv import load_dotenv
import os
import logging
import yaml
from telethon import TelegramClient, events, errors
from lemmatization import lemmatize

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

logging.warning('bot started...')

env = os.getenv('ENV', 'dev')  # Default to 'prod' if ENV is not set
config_file_name = 'config.dev.yaml' if env == 'dev' else 'config.yaml'

api_id = int(os.getenv('TELEGRAM_API_ID', 0))
api_hash = str(os.getenv('TELEGRAM_API_HASH'))
chat_send_to = str(os.getenv('TELEGRAM_CHAT_SEND_TO'))

# Load the configuration from the YAML file
with open(config_file_name, encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

# Extract chat URLs and keywords from the config
chat_urls = config['chats']
keywords = set(config['keywords'])

joined_keywords = ' '.join(keywords)
lemmatized_keywords = sorted(lemmatize(joined_keywords))

keywords_not_in_lemmatized = [word for word in keywords if word not in lemmatized_keywords]
logging.warning(keywords_not_in_lemmatized)

# Global set to store hashes of sent messages
sent_messages_cache = set()

# Initialize the client
client = TelegramClient('catebi_freegan', api_id, api_hash)

@client.on(events.NewMessage(chats=chat_urls))
async def new_message_listener(event):
    # Process the text of the event to get lemmas
    lemmas = lemmatize(event.text)
    matched_keywords = lemmas.intersection(keywords)

    if matched_keywords:
        # Get the sender of the message
        sender = await event.get_sender()
        sender_name = "@" + getattr(sender, 'username', 'Unknown')

        # Compute the hash of the message
        message_hash = hash(f"{sender_name}_{event.text}")

        # Check if the message has already been sent
        if message_hash not in sent_messages_cache:
            matched_keywords_str = ', '.join(matched_keywords)
            message = f"**{matched_keywords_str}**\n\n{event.text}\n\n[t.me/{event.chat.username}/{event.id}](t.me/{event.chat.username}/{event.id})\nuser: {sender_name}"
            await client.send_message(chat_send_to, message, file=event.photo)
            sent_messages_cache.add(message_hash)

def main():
    logging.warning('[main]started..')
    try:
        client.start()
        logging.warning("Client is connected.")
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