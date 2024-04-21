import os
import requests
from dotenv import load_dotenv
from functools import lru_cache


class EnvProcessor:
    load_dotenv()

    @staticmethod
    def _get_env(name, default=None):
        return os.getenv(name, default)

    @classmethod
    def get_env_variables(cls, prefix):
        variables = []
        i = 1
        while True:
            value = cls._get_env(f'{prefix}_{i}')
            if value is None:
                break
            variables.append(value)
            i += 1
        return variables

    @staticmethod
    @lru_cache()
    def read_api_id():
        return int(EnvProcessor._get_env('TELEGRAM_API_ID', 0))

    @staticmethod
    @lru_cache()
    def read_api_hash():
        return EnvProcessor._get_env('TELEGRAM_API_HASH', '')

    @staticmethod
    @lru_cache()
    def read_chat_send_to():
        return EnvProcessor._get_env('TELEGRAM_CHAT_SEND_TO', '')

    @staticmethod
    @lru_cache()
    def read_developers():
        return EnvProcessor.get_env_variables('DEVELOPER')

    @staticmethod
    @lru_cache()
    def read_system_topic_id():
        return int(EnvProcessor._get_env('TOPIC_ID', 0))

    @staticmethod
    @lru_cache()
    def read_chat_urls():
        if EnvProcessor._get_env('ENV', 'dev') == 'dev':
            return EnvProcessor.get_env_variables('CHAT')
        else:
            response = requests.get('example.api')
            return [x['url'] for x in response.json()]


# Cached properties
API_ID = EnvProcessor.read_api_id()
API_HASH = EnvProcessor.read_api_hash()
CHAT_SEND_TO = EnvProcessor.read_chat_send_to()
DEVELOPERS = EnvProcessor.read_developers()
SYSTEM_TOPIC_ID = EnvProcessor.read_system_topic_id()
CHAT_URLS = EnvProcessor.read_chat_urls()
