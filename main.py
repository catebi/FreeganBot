import asyncio
import logging
import signal
from logging import DEBUG, INFO

from telethon import TelegramClient

from telegram_api.error_handler import ErrorHandler
from telegram_api.telegram_adapter import TelegramAdapter
from utils.env_processor import EnvProcessor

CHAT_LOGGING_LEVEL = INFO
CONSOLE_LOGGING_LEVEL = DEBUG


async def main():
    client = TelegramClient('catebi_freegan', EnvProcessor.api_id(), EnvProcessor.api_hash(),
                            sequential_updates=True)
    error_handler = ErrorHandler(client)
    adapter = TelegramAdapter(error_handler)
    signal.signal(signal.SIGTERM, lambda sig, frame: asyncio.create_task(adapter.signal_handler(sig, frame)))
    await adapter.run_client(client)


if __name__ == "__main__":
    logging.basicConfig(level=CONSOLE_LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main())
