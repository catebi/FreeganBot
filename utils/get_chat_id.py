import asyncio
from typing import Optional

from telethon import TelegramClient

from utils.env_processor import EnvProcessor

CHAT_URL: Optional[str] = "https://t.me/test_freegan_mariam"  # Do not forget to insert URL of public chat here!


async def get_chat_id(client: TelegramClient, chat_username: str):
    """
        Asynchronously retrieves and prints the negative of the chat ID from a specified chat username.

        Parameters:
        - client (TelegramClient): An instance of TelegramClient to communicate with Telegram API.
        - chat_username (str): The username of the chat from which to retrieve the ID.

        The function sends a message to the specified chat and prints the chat ID by accessing the `channel_id`
        from the response, negating it to conform with Telegram's ID conventions.
    """
    message_content = f"Message to get chat id"
    res = await client.send_message(chat_username, message_content)
    print(f"Id for chat {chat_username} is {res.peer_id.channel_id * (-1)}")


async def run_chat_id_retrieving_client(chat_username: str):
    """
        Asynchronously creates a Telegram client and retrieves the chat ID for a given username.

        Parameters:
        - chat_username (str): The username of the chat for which the ID needs to be retrieved.

        This function initializes a TelegramClient and then calls `get_chat_id`
    """
    if chat_username:
        client = TelegramClient('catebi_freegan', EnvProcessor.api_id(), EnvProcessor.api_hash(),
                                sequential_updates=True)
        async with client:
            await get_chat_id(client, chat_username)
    else:
        print("Please, insert chat URL into CHAT_URL variable")


if __name__ == "__main__":
    asyncio.run(run_chat_id_retrieving_client(CHAT_URL))
