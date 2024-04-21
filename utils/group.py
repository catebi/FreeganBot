class Group:
    """
    Represents a group with specific keyword filtering criteria.

    This class is used to store information about a specific group including its name
    and various sets of keywords associated with it.

    Attributes:
        group_name (str): The name of the group.
        keywords (set[str]): The set of primary search keywords associated with this group.
        include_keywords (set[str]): Keywords that should be included in a message to be associated with this group.
        exclude_keywords (set[str]): Keywords that should NOT be included in a message to be associated with this group.
    """

    def __init__(self, group_name, keywords, include_keywords, exclude_keywords):
        """
        Initializes a new instance of the Group class with the specified name, keywords,
        and inclusion/exclusion criteria.
        """
        self.group_name = group_name
        self.keywords = keywords
        self.include_keywords = include_keywords
        self.exclude_keywords = exclude_keywords
