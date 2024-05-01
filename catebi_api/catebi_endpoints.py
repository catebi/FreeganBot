from functools import lru_cache


class CatebiEndpoints:

    @classmethod
    @lru_cache()
    def save_reaction(cls) -> str:
        """Return save reaction endpoint URL. """
        return "https://api.catebi.ge/api/Freegan/SaveReaction"

    @classmethod
    @lru_cache()
    def save_message(cls) -> str:
        """Return save message endpoint URL. """
        return "https://api.catebi.ge/api/Freegan/SaveMessage"
