import re
from datetime import datetime

from catebi_api.catebi_adapter import save_reaction


async def get_sender_username(event):
    sender = await event.get_sender()
    sender_username = getattr(sender, 'username', None)
    display_username = f"@{sender_username}" if sender_username else "an anonymous user"
    return sender, display_username


async def prepare_message_hash_and_photos(client, event):
    sanitized_event_text = re.sub(r'\s+', '', event.text)
    message_hash = hash(sanitized_event_text)
    photos = event.media
    if event.grouped_id:
        photos = await collect_grouped_media(client, event)
    return message_hash, photos


async def collect_grouped_media(client, event):
    photos = [event.media]
    async for mess in client.iter_messages(event.chat.username, min_id=event.id,
                                           max_id=event.id + 10, reverse=True):
        if mess.grouped_id == event.grouped_id:
            photos.append(mess.media)
        else:
            break
    return photos


def get_current_time():
    """ Returns the current time formatted as HH:MM:SS.mmm """
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


async def save_message_reaction(text, response, photos):
    new_message_id = response[0].id if isinstance(photos, list) else response.id
    data = {'messageId': new_message_id, 'content': text, 'likeCount': 0, 'dislikeCount': 0}
    save_reaction(data)
