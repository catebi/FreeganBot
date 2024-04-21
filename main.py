from dotenv import load_dotenv
import asyncio
import signal
import os
import logging
import yaml
import re
from telethon import TelegramClient, events, errors, functions
from telethon.tl.types import UpdateMessageReactions
from datetime import datetime
import requests
from logging import DEBUG, INFO, ERROR

from utils.lemmatizer import Lemmatizer

CHAT_LOGGING_LEVEL = INFO
CONSOLE_LOGGING_LEVEL = DEBUG

API_SAVEMESSAGE_METHOD = 'https://api.catebi.ge/api/Freegan/SaveMessage'

# Load environment variables from .env file
load_dotenv()
env = os.getenv('ENV', 'dev')  # Default to 'dev' if ENV is not set
config_file_name = 'config.yaml'
api_id = int(os.getenv('TELEGRAM_API_ID', 0))
api_hash = str(os.getenv('TELEGRAM_API_HASH'))
chat_send_to = str(os.getenv('TELEGRAM_CHAT_SEND_TO'))
messages_collecting_is_on = str(os.getenv('MESSAGES_COLLECTING_IS_ON'))


# Function to get multiple environment variables with similar names
def get_env_variables(prefix):
    variables = []
    i = 1
    while True:
        value = os.getenv(f'{prefix}_{i}')
        if value is None:
            break
        variables.append(value)
        i += 1
    return variables


# Retrieve developers from environment
developers = get_env_variables('DEVELOPER')
print(developers)

# Retrieve topic ID from environment (assuming it's a single value)
system_topic_id = int(os.getenv('TOPIC_ID'))
print(system_topic_id)

chat_urls = get_env_variables('CHAT') if env == 'dev' else list(
    map(lambda x: x['url'], requests.get('https://api.catebi.ge/api/freegan/getdonationchats').json()))

# retrieve groups with filters from config
with open(config_file_name, encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

groups_data = {}
for group in config['groups']:
    group_name = group['name']
    keywords = set(group['keywords'])
    include_keywords = set(group.get('include_keywords', []))
    exclude_keywords = set(group.get('exclude_keywords', []))
    groups_data[group_name] = {
        'keywords': keywords,
        'include_keywords': include_keywords,
        'exclude_keywords': exclude_keywords
    }

# Global set to store hashes of sent messages
sent_messages_cache = set()

# Global Telegram client variable
client = None


async def new_message_listener(client, event):
    if not event.text:
        logging.info('%s%s', event.id, 'empty event.text')
        return
    # Process the text of the event to get lemmas
    lemmatizer = Lemmatizer()
    lemmas = lemmatizer.lemmatize(event.text + ' ' + event.text.replace('-', ''))

    matched_keywords = set()

    # Calculate intersections and apply rules based on the new groups structure
    for name, info in groups_data.items():
        intersection_keywords = lemmas.intersection(info['keywords'])
        intersection_include = lemmas.intersection(info['include_keywords'])
        intersection_exclude = lemmas.intersection(info['exclude_keywords'])

        if intersection_keywords:
            if (info['include_keywords'] and intersection_include) or (
                    info['exclude_keywords'] and not intersection_exclude):
                matched_keywords.update(intersection_keywords)

    post_message_to_db_archive(event.text, (' ').join(lemmas), f"https://t.me/{event.chat.username}/{event.id}", bool(matched_keywords), messages_collecting_is_on)

    if matched_keywords:
        # Get the sender of the message
        sender = await event.get_sender()

        sender_username = getattr(sender, 'username', None)
        display_username = f"@{sender_username}" if sender_username else "an anonymous user"

        sanitized_event_text = re.sub(r'\s+', '', event.text)
        message_hash = hash(sanitized_event_text)

        photos = event.media

        # Check if the message has already been sent
        if message_hash not in sent_messages_cache:
            if event.grouped_id:
                photos = [photos]
                async for mess in client.iter_messages(event.chat.username, min_id=event.id, max_id=event.id + 10,
                                                       reverse=True):
                    if mess.grouped_id == event.grouped_id:
                        photos.append(mess.media)
                    else:
                        break
            matched_keywords_str = ', '.join(matched_keywords)
            current_time = get_current_time()
            message = (f"**{matched_keywords_str}**\n\n{event.text}\n\n"
                       f"[t.me/{event.chat.username}/{event.id}](t.me/{event.chat.username}/{event.id})\n"
                       f"user: {display_username}\n\n"
                       f"__time__: `{current_time}`\n"
                       f"__hash__: `{message_hash}`\n")
            res = await client.send_message(chat_send_to, message, file=photos)
            new_message_id = res[0].id if isinstance(photos, list) else res.id
            data = {'messageId': new_message_id,
                    'content': event.text,
                    'likeCount': 0,
                    'dislikeCount': 0,
                    }
            requests.post('https://api.catebi.ge/api/Freegan/SaveReaction', json=data,
                          headers={'Content-type': 'application/json'})
            sent_messages_cache.add(message_hash)
            await asyncio.sleep(0.3)  # Delay for 100 milliseconds


def post_message_to_db_archive(originalText, lemmatizedText, chatLink, accepted, on):
    if on:
        archive_post_data = {
            'originalText': originalText,
            'lemmatizedText': lemmatizedText,
            'chatLink': chatLink,
            'accepted': accepted
        }
        try:
            response = requests.post(API_SAVEMESSAGE_METHOD, json=archive_post_data,
                                     headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        except requests.RequestException as e:
            debug(f"An error occurred: {e}", level=ERROR)
            raise
    if response.status_code == 200:
        logging.debug('response: "%s"', response.text)
    else:
        debug(f'{API_SAVEMESSAGE_METHOD} status_code: {response.status_code}',
              level=ERROR if response.status_code >= 400 else INFO)
    return response.status_code


async def reaction_listener(event):
    if (event.top_msg_id and event.top_msg_id != system_topic_id):
        like_count = dislike_count = 0
        if event.reactions.results:
            for react in event.reactions.results:
                if react.reaction.emoticon == '👍':
                    like_count = react.count
                else:
                    dislike_count = react.count
        data = {'messageId': event.msg_id,
                'content': '',
                'likeCount': like_count,
                'dislikeCount': dislike_count,
                }
        requests.post('https://api.catebi.ge/api/Freegan/SaveReaction', json=data,
                      headers={'Content-type': 'application/json'})


async def debug(message, level=DEBUG):
    # Log the message
    logging.log(level, message)
    
    # Check the current logging level
    if level >= CHAT_LOGGING_LEVEL:
        formatted_message = f"[{logging.getLevelName(level)}] {message}"

        # Send the message using the provided Telegram client
        await client.send_message(chat_send_to, formatted_message)

def get_current_time():
    """ Returns the current time formatted as HH:MM:SS.mmm """
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# Define your signal handler
async def signal_handler(sig, frame):
    print(sig, frame)
    global client
    if client:
        await debug("Freegan has stopped", INFO)
        client.disconnect()


async def check(client):
    dialogs = [f'https://t.me/{dialog.draft.entity.username}' async for dialog in client.iter_dialogs() if
               dialog.is_channel and dialog.draft.entity.username]
    for chat in chat_urls:
        if chat not in dialogs:
            try:
                await client(functions.channels.JoinChannelRequest(chat))
            except errors.ChannelsTooMuchError:
                await client.send_message(chat_send_to,
                                          f"{developers}, I've joined too many channels and I can't join{chat}")
            except errors.InviteRequestSentError:
                await client.send_message(chat_send_to, f"{developers}, a request has been sent to join {chat}")
            except errors.ChannelPrivateError:
                await client.send_message(chat_send_to, f"{developers}, there is no permission to access {chat}")
            except errors.ChannelInvalidError as e:
                await client.send_message(chat_send_to, f"{developers}, {e} {chat}")
            except BaseException as e:
                await client.send_message(chat_send_to, f"{developers}, {e} {chat}")
                chat_urls.remove(chat)


async def run_client():
    global client
    client = TelegramClient('catebi_freegan', api_id, api_hash, sequential_updates=True)
    # Register your event handlers here
    client.add_event_handler(lambda event: new_message_listener(client, event), events.NewMessage(chats=chat_urls))
    client.add_event_handler(lambda event: reaction_listener(event), events.Raw(UpdateMessageReactions))

    async with client:
        await check(client)
        try:
            await debug("Freegan has started", INFO)
            await client.run_until_disconnected()
        except Exception as e:
            # Log and send a message if an error occurs
            await debug(f"An unexpected error occurred: {e}", ERROR)
        finally:
            # check if client is disconnected
            if client.is_connected():
                await debug('strange thing happened', ERROR)
                client.disconnect()


async def main():
    signal.signal(signal.SIGTERM, lambda sig, frame: asyncio.create_task(signal_handler(sig, frame)))
    await run_client()


if __name__ == "__main__":
    logging.basicConfig(level=CONSOLE_LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main())
