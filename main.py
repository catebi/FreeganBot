from dotenv import load_dotenv
import os
import logging
import yaml
from telethon import TelegramClient, events, errors
from datetime import datetime
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

keyword_group_1 = set(config['keyword_group_1'])
keyword_group_2 = set(config['keyword_group_2'])
keyword_group_3 = set(config['keyword_group_3'])
keyword_group_4 = set(config['keyword_group_4'])
filter_keyword_group_2 = set(config['filter_keyword_group_2'])
filter_keyword_group_3 = set(config['filter_keyword_group_3'])
filter_keyword_group_4 = set(config['filter_keyword_group_4'])

# Global set to store hashes of sent messages
sent_messages_cache = set()

client = TelegramClient('catebi_freegan', api_id, api_hash)

@client.on(events.NewMessage(chats=chat_urls))
async def new_message_listener(event):
    # Process the text of the event to get lemmas
    lemmas = lemmatize(event.text)

    # Calculate intersections of lemmas with keyword groups
    intersection_group_1 = lemmas.intersection(keyword_group_1)
    intersection_group_2 = lemmas.intersection(keyword_group_2)
    intersection_group_3 = lemmas.intersection(keyword_group_3)
    intersection_group_4 = lemmas.intersection(keyword_group_4)

    intersection_filter_2 = lemmas.intersection(filter_keyword_group_2)
    intersection_filter_3 = lemmas.intersection(filter_keyword_group_3)
    intersection_filter_4 = lemmas.intersection(filter_keyword_group_4)

    matched_keywords = set()

    # Check for matches and update matched_keywords accordingly
    if intersection_group_1:
        matched_keywords.update(intersection_group_1)
    if intersection_group_2 and intersection_filter_2:
        matched_keywords.update(intersection_group_2)
    if intersection_group_3 and intersection_filter_3:
        matched_keywords.update(intersection_group_3)
    if intersection_group_4 and intersection_filter_4:
        matched_keywords.update(intersection_group_4)

    if matched_keywords:
        # Get the sender of the message
        sender = await event.get_sender()

        sender_username = getattr(sender, 'username', None)
        display_username = f"@{sender_username}" if sender_username else "an anonymous user"

        message_hash = hash(f"{display_username}_{event.text}")

        photos = event.photo

        # Check if the message has already been sent
        if message_hash not in sent_messages_cache:
            if event.grouped_id:
                photos = [photos]
                async for mess in client.iter_messages(event.chat.username, min_id=event.id, max_id=event.id + 10, reverse=True):
                    if mess.grouped_id == event.grouped_id:
                        if mess.photo:  # Check if there is a photo to avoid None
                            photos.append(mess.photo)
                    else:
                        break
            matched_keywords_str = ', '.join(matched_keywords)
            current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            message = (f"**{matched_keywords_str}**\n\n{event.text}\n\n"
                       f"[t.me/{event.chat.username}/{event.id}](t.me/{event.chat.username}/{event.id})\n"
                       f"user: {display_username}\n\n"
                       f"__time__: `{current_time}`\n"
                       f"__hash__: `{message_hash}`\n")
            await client.send_message(chat_send_to, message, file=photos)
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
