import os
import requests
from dotenv import load_dotenv
from functools import lru_cache


class EnvProcessor:
    """
    A utility class for managing and retrieving environment variables.
    The class provides methods to fetch individual or groups of environment variables.
    """

    load_dotenv()  # Load environment variables from a .env file at start-up.

    @staticmethod
    def _get_env(name: str, default=None) -> str:
        """
        Fetch environment variable values.

        Args:
            name (str): The name of the environment variable to retrieve.
            default (any): The default value to return if the environment variable is not found.

        Returns:
            str: The value of the environment variable or the default value if not set.
        """
        return os.getenv(name, default)

    @classmethod
    def get_env_variables(cls, prefix: str) -> list[str]:
        """
        Retrieve a list of environment variables that begin with a given prefix.

        Args:
            prefix (str): A common prefix for the environment variables to be retrieved.

        Returns:
            list[str]: A list of values for the found environment variables.
        """
        variables = []
        i = 1
        while True:
            var_name = f"{prefix}_{i}"
            value = cls._get_env(var_name)
            if value is None:
                break
            variables.append(value)
            i += 1
        return variables

    @classmethod
    @property
    @lru_cache()
    def api_id(cls) -> int:
        """Return the Telegram API ID as an integer."""
        return int(cls._get_env('TELEGRAM_API_ID', 0))

    @classmethod
    @property
    @lru_cache()
    def api_hash(cls) -> str:
        """Return the Telegram API hash as a string."""
        return cls._get_env('TELEGRAM_API_HASH', '')

    @classmethod
    @property
    @lru_cache()
    def chat_send_to(cls) -> str:
        """Return the identifier where Telegram messages should be sent."""
        return cls._get_env('TELEGRAM_CHAT_SEND_TO', '')

    @classmethod
    @property
    @lru_cache()
    def system_topic_id(cls) -> int:
        """Return the system topic ID as an integer."""
        return int(cls._get_env('TOPIC_ID', 0))

    @classmethod
    @property
    @lru_cache()
    def chat_urls(cls) -> list[str]:
        """
        Return a list of chat URLs.
        """
        if cls._get_env('ENV', 'dev') == 'dev':
            return cls.get_env_variables('CHAT')
        else:
            response = requests.get('example.api')
            return [x['url'] for x in response.json()]

    @classmethod
    @property
    @lru_cache()
    def developers(cls) -> list[str]:
        """Return a list of developers from environment variables."""
        return cls.get_env_variables('DEVELOPER')
