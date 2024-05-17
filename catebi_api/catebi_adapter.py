from typing import Optional

import requests
from requests import Response

from catebi_api.catebi_endpoints import CatebiEndpoints


def post_message_to_db_archive(original_text: str, lemmatized_text: str, chat_link: str, accepted: bool,
                               message_collecting_is_on: bool) -> Optional[Response]:
    """
    Posts a message to a database archive, if message collecting is enabled.

    Parameters:
        original_text (str): The original text of the message to archive.
        lemmatized_text (str): The lemmatized version of the original text.
        chat_link (str): The URL linking to the location of the chat.
        accepted (bool): Indicates whether the message was accepted or not.
        message_collecting_is_on (bool): Flag to check if the message collecting feature is turned on.

    Returns:
        Optional[Response]: The response object from the request if the request is made; otherwise, None.

    Raises:
        RequestException: If there is an issue with making the HTTP request.
    """
    if message_collecting_is_on:
        archive_post_data = {
            'originalText': original_text,
            'lemmatizedText': lemmatized_text,
            'chatLink': chat_link,
            'accepted': accepted
        }
        return requests.post(CatebiEndpoints.save_message(), json=archive_post_data,
                             headers={'Content-type': 'application/json', 'Accept': 'text/plain'})


def save_reaction(data: dict) -> None:
    """
    Sends a post request to the API with reaction data
    including message ID, content of the message, and like/dislike counts.

    Parameters:
        data (dict): A dictionary containing the following keys:
                     - 'messageId' (int): The ID of the message.
                     - 'content' (str): The text of the message.
                     - 'likeCount' (int): Number of likes for the message.
                     - 'dislikeCount' (int): Number of dislikes for the message.

    Returns:
        None: This function does not return anything.

    Raises:
        RequestException: If there is an issue with making the HTTP request.
    """
    requests.post(CatebiEndpoints.save_reaction(), json=data,
                  headers={'Content-type': 'application/json'})

