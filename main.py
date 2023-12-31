from dotenv import load_dotenv
import asyncio
import signal
import os
import logging
import yaml
import re
from telethon import TelegramClient, events, errors
from datetime import datetime
from lemmatization import lemmatize

# Debug level constants
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# Debug level names
LEVEL_NAMES = {
    DEBUG: "DEBUG",
    INFO: "INFO",
    WARNING: "WARNING",
    ERROR: "ERROR",
    CRITICAL: "CRITICAL"
}

# Load environment variables from .env file
load_dotenv()

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

# Global Telegram client variable
client = None

async def new_message_listener(client, event):
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

        sanitized_event_text = re.sub(r'\s+', '', event.text)
        message_hash = hash(f"{display_username}_{sanitized_event_text}")

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
            current_time = get_current_time()
            message = (f"**{matched_keywords_str}**\n\n{event.text}\n\n"
                       f"[t.me/{event.chat.username}/{event.id}](t.me/{event.chat.username}/{event.id})\n"
                       f"user: {display_username}\n\n"
                       f"__time__: `{current_time}`\n"
                       f"__hash__: `{message_hash}`\n")
            await client.send_message(chat_send_to, message, file=photos)

            sent_messages_cache.add(message_hash)
            await asyncio.sleep(0.3)  # Delay for 100 milliseconds

async def debug(client, message, level=DEBUG):
    # Check the current logging level
    if logging.getLogger().level <= level:
        level_name = LEVEL_NAMES.get(level, "UNKNOWN")
        formatted_message = f"[{level_name}] {message}"

        # Log the message
        if level == DEBUG:
            logging.debug(formatted_message)
        elif level == INFO:
            logging.info(formatted_message)
        elif level == WARNING:
            logging.warning(formatted_message)
        elif level == ERROR:
            logging.error(formatted_message)
        elif level == CRITICAL:
            logging.critical(formatted_message)

        # Send the message using the provided Telegram client
        await client.send_message(chat_send_to, formatted_message)

def get_current_time():
    """ Returns the current time formatted as HH:MM:SS.mmm """
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

# Define your signal handler
async def signal_handler(sig, frame):
    global client
    if client:
        await debug(client, "Freegan has stopped", INFO)
        client.disconnect()

async def run_client():
    global client
    client = TelegramClient('catebi_freegan', api_id, api_hash)
    # Register your event handlers here
    client.add_event_handler(lambda event: new_message_listener(client, event), events.NewMessage(chats=chat_urls))

    async with client:
        try:
            await debug(client, "Freegan has started", INFO)
            await client.run_until_disconnected()
        except Exception as e:
            # Log and send a message if an error occurs
            await debug(client,  f"An unexpected error occurred: {e}", ERROR)
        finally:
            # check if client is disconnected
            if client.is_connected():
                await client.send_message(chat_send_to, "strange thing happened")
                client.disconnect()

async def main():
    signal.signal(signal.SIGTERM, lambda sig, frame: asyncio.create_task(signal_handler(sig, frame)))
    await run_client()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(run_client())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main())