from functools import lru_cache
from typing import Any

import yaml
from utils.group import Group


class YamlProcessor:
    """
    A processor class for handling YAML configuration file.
    The class provides methods to load configuration from a YAML file, read group
    data, and caches these operations to improve performance on repeated accesses.
    """

    @classmethod
    def config_name(cls) -> str:
        """
        Returns the name of the YAML configuration file.
        """
        return 'config.yaml'

    @classmethod
    @lru_cache()
    def config(cls) -> Any:
        """
        Loads the YAML configuration file specified by `config_name`.
        """
        with open(cls.config_name(), encoding="utf-8") as config_file:
            return yaml.safe_load(config_file)

    @classmethod
    def read_groups(cls) -> list[Group]:
        """
        Parses the 'groups' data from the YAML configuration file and creates a list of Group
        objects with the specified properties.
        """
        groups_data = []
        for group in cls.config()['groups']:
            group_name = group['name']
            keywords = set(group['keywords'])
            include_keywords = set(group.get('include_keywords', []))
            exclude_keywords = set(group.get('exclude_keywords', []))
            groups_data.append(Group(group_name=group_name, keywords=keywords,
                                     include_keywords=include_keywords, exclude_keywords=exclude_keywords))
        return groups_data

    @classmethod
    @lru_cache()
    def groups_data(cls) -> list[Group]:
        """
        Cached property that parses and returns the list of groups from the YAML configuration.
        """
        return cls.read_groups()
