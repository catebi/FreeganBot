import asyncio
import logging
from logging import ERROR, INFO

from telethon import events, functions
from telethon.tl.types import UpdateMessageReactions

from catebi_api.catebi_adapter import save_reaction, post_message_to_db_archive
from text_processing.text_processor import process_text_and_extract_keywords
from utils.env_processor import EnvProcessor
from utils.telegram_utils import get_sender_username, prepare_message_hash_and_photos, get_current_time, \
    save_message_reaction


class TelegramAdapter:
    def __init__(self, error_handler):
        self.client = None
        self.sent_messages_cache = set()
        self.error_handler = error_handler

    async def new_message_listener(self, event):
        if not event.text:
            logging.info('%s empty event.text', event.id)
            return

        lemmas, matched_keywords = process_text_and_extract_keywords(event.text)

        # Posting the message to the database and handling the response
        await self.handle_database_posting(event, lemmas, matched_keywords)

        if matched_keywords:
            await self.process_matched_keywords(event, matched_keywords)

    @classmethod
    async def reaction_listener(cls, event):
        if event.top_msg_id and event.top_msg_id != EnvProcessor.system_topic_id():
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
            save_reaction(data)

    async def run_client(self, client):
        self.client = client

        self.client.add_event_handler(lambda event: self.new_message_listener(event),
                                      events.NewMessage(chats=EnvProcessor.chat_urls()))
        self.client.add_event_handler(lambda event: self.reaction_listener(event), events.Raw(UpdateMessageReactions))

        async with self.client:
            await self.check()
            try:
                await self.error_handler.send_log("Freegan has started", INFO)
                await self.client.run_until_disconnected()
            except Exception as e:
                await self.error_handler.send_log(f"An unexpected error occurred: {e}", ERROR)
            finally:
                if self.client.is_connected():
                    await self.error_handler.send_log('strange thing happened', ERROR)
                    self.client.disconnect()

    async def process_matched_keywords(self, event, matched_keywords):
        sender, display_username = await get_sender_username(event)
        message_hash, message_photos = await prepare_message_hash_and_photos(self.client, event)
        if message_hash not in self.sent_messages_cache:
            await self.send_message_with_media(event, matched_keywords, display_username, message_hash, message_photos)
            self.sent_messages_cache.add(message_hash)

    async def send_message_with_media(self, event, matched_keywords, display_username, message_hash, photos):
        matched_keywords_str = ', '.join(matched_keywords)
        current_time = get_current_time()
        message_content = (f"**{matched_keywords_str}**\n\n{event.text}\n\n"
                           f"[t.me/{event.chat.username}/{event.id}](t.me/{event.chat.username}/{event.id})\n"
                           f"user: {display_username}\n\n"
                           f"__time__: `{current_time}`\n"
                           f"__hash__: `{message_hash}`\n")
        res = await self.client.send_message(EnvProcessor.chat_send_to(), message_content, file=photos)
        await save_message_reaction(event.text, res, photos)
        await asyncio.sleep(0.3)

    async def signal_handler(self, sig, frame):
        print(sig, frame)
        if self.client:
            await self.error_handler.send_log("Freegan has stopped", INFO)
            self.client.disconnect()

    async def check(self):
        dialogs = [f'https://t.me/{dialog.draft.entity.username}' async for dialog in self.client.iter_dialogs() if
                   dialog.is_channel and dialog.draft.entity.username]
        for chat in EnvProcessor.chat_urls():
            if chat not in dialogs:
                try:
                    await self.client(functions.channels.JoinChannelRequest(chat))  # type: ignore
                except Exception as e:
                    self.error_handler.send_exception_error(chat, e)

    async def handle_database_posting(self, event, lemmas, matched_keywords):
        return await self.error_handler.send_api_log(post_message_to_db_archive, event.text, ' '.join(lemmas),
                                                     f"https://t.me/{event.chat.username}/{event.id}",
                                                     bool(matched_keywords), EnvProcessor.message_collecting_is_on())
