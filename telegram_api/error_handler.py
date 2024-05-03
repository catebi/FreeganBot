import logging
from logging import DEBUG

import requests
from telethon import errors

from utils.env_processor import EnvProcessor


class ErrorHandler:
    def __init__(self, client):
        self.client = client

    @classmethod
    def errors_messages_map(cls, chat, exception):
        return {errors.ChannelsTooMuchError:
                f"{EnvProcessor.developers()}, I've joined too many channels and I can't join {chat}",
                errors.InviteRequestSentError: f"{EnvProcessor.developers()}, a request has been sent to join {chat}",
                errors.ChannelPrivateError: f"{EnvProcessor.developers()}, there is no permission to access {chat}",
                errors.ChannelInvalidError: f"{EnvProcessor.developers()}, {exception} {chat}",
                }

    async def send_exception_error(self, chat, exception):
        error_type = type(exception)
        if message_template := self.errors_messages_map(chat, exception).get(error_type):
            error_message = message_template.format(chat=chat, e=exception)
            await self.client.send_message(EnvProcessor.chat_send_to(), error_message)
        else:
            # Handle unknown exception types if needed
            default_message = f"{EnvProcessor.developers()}, an unexpected error type {error_type.__name__} " \
                              f"occurred: {str(exception)} "
            await self.client.send_message(EnvProcessor.chat_send_to(), default_message)
        EnvProcessor.chat_urls().remove(chat)

    async def send_log(self, message, level=DEBUG):
        formatted_message = f"[{logging.getLevelName(level)}] {message}"
        await self.client.send_message(EnvProcessor.chat_send_to(), formatted_message)

    async def send_api_log(self, func, *args, **kwargs):
        try:
            response = func(*args, **kwargs)
            if response and response.status == 200:
                logging.debug('API Call Successful: %s', response.text)
            elif response:
                log_level = logging.ERROR if response.status >= 400 else logging.INFO
                await self.send_log(
                    f'API Error with status {response.status}: {response.text}',
                    level=log_level)
            return response
        except requests.RequestException as e:
            await self.send_log(f"API request failed: {e}", level=logging.ERROR)
