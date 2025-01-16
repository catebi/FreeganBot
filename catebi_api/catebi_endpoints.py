from functools import lru_cache

from utils.env_processor import EnvProcessor


class CatebiEndpoints:

    @classmethod
    @lru_cache()
    def save_reaction(cls) -> str:
        """Return save reaction endpoint URL. """
        return f"{EnvProcessor.catebi_api()}/Freegan/SaveReaction"

    @classmethod
    @lru_cache()
    def save_message(cls) -> str:
        """Return save message endpoint URL. """
        return f"{EnvProcessor.catebi_api()}/Freegan/SaveMessage"
