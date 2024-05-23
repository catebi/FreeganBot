# FreeganBot

Telegram bot to search for donations in chats and channels

## Install Guide

### Prerequisites

1. [x] **Python Installation**: This script requires Python, specifically version 3.13, due to compatibility with libraries
   used. Here are the steps to install Python 3.13:

    - **Ubuntu/Linux**:
      ```bash
      sudo add-apt-repository ppa:deadsnakes/ppa
      sudo apt update
      sudo apt install python3.13 python3.13-venv python3.13-dev
      ```

    - **Windows**:
      Download and install Python 3.13 from [Python Releases for Windows](https://www.python.org/downloads/windows/). During installation, make sure to check the
      option 'Add Python 3.13 to PATH'.

    - **macOS**:
      Install Homebrew if it's not already installed:
      ```bash
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
      Then, install Python 3.13 using Homebrew:
      ```bash
      brew install python@3.13
      brew link --overwrite python@3.13
      ```

   Verify the installation by checking the Python version:
   ```bash
   python3.13 --version
   ```
2. [x] **Setting Up Venv**: First, create [venv](https://docs.python.org/3/library/venv.html) for the project with this
   command:
   ```bash
   python3.13 -m venv venv
   ```
   Next, activate venv:
   ```bash
   source venv/bin/activate
   ```
3. [x] **Install Dependencies**: install all required dependencies with
   this [command](https://pip.pypa.io/en/stable/user_guide/):

   ```bash
   pip install -r requirements.txt
   ```
4. [x] **Telegram API Credentials**: You need a Telegram API `api_id` and `api_hash`. These are obtained by registering your
   application on Telegram’s website. Here's how:

    - Go to [my.telegram.org](https://my.telegram.org).
    - Log in with your Telegram account.
    - Click on 'API development tools' and fill out the form to create a new application.
    - Once created, you'll receive your `api_id` and `api_hash`.
5. [x] **Internet Connection**: Since the script interacts with Telegram's servers, an active internet connection is
   required.
6. [x] **A Telegram Account**: The script will run under your Telegram account, so ensure you have access to the account you
   intend to use.
7. [x] **Environment Variables**: copy `env.example` content into `.env` file with this command:
   ```bash
   [ ! -f .env ] && cp env.example .env
   ```
   And insert these variables into your `.env` file:

    - `ENV` is prod/dev (dev is default).
    - `TELEGRAM_API_ID` is from [my.telegram.org](https://my.telegram.org) `api_id`.
    - `TELEGRAM_API_HASH` is from [my.telegram.org](https://my.telegram.org) `api_hash`.
    - `TELEGRAM_CHAT_SEND_TO` is Telegram Chat ID where bot should send donation messages to (for dev purposes it's
      usually your test chat).
   
    **Attention**! To get Chat ID, you should copy your public chat URL and insert it into "CHAT_URL" in [get_chat_id](./utils/get_chat_id.py) script.

    Once you've done it, run the script. You see the output like:

    ```
    Id for chat YOUR_CHAT_URL is -YOUR_CHAT_ID
    ```

    Copy chat ID (exactly negative number!) into `TELEGRAM_CHAT_SEND_TO` env variable.

9. [x] **Setting up your test environment**: You should test the bot functions with your test chat. Here's how to do that:

    - Create a public chat or channel in Telegram
    - Add [@freegan_catebi_leshiy_bot](https://t.me/freegan_catebi_leshiy_bot) into your chat
    - Give it Admin role and make sure bot is allowed to send messages in the chat

### Additional Description

- At the first launch, in the terminal you will need to enter the phone number to which your Telegram account is linked
- You can read about TelegramClient methods [here](https://docs.telethon.dev/en/stable/modules/client.html)
- When the program runs, it creates `catebi_freegan.session` file with information about the session, so that in the
  future do not re-enter the data (in general, user (bot) data can be written in the code)

### Troubleshooting

- in the Chat library - a small group chat (group) - and Channel are different concepts, and the message reference part
  of the code only works with Channel. It's hard to encounter anything in nature that isn't a channel and causes an
  error unless you create a small closed group and send messages to yourself. Anything with a public username is already
  a channel.
- The user or bot must be a member of the group from which it is planned to send messages.

## Bot Config

Bot config is `config.yaml` file.

Config structure:

   ```yaml
   chats:
     - <telegramChatUrl1>
     - <telegramChatUrl2>

   sys_logging:
     developers: "@<telegramAccount1Name>, @<telegramAccount2Name>"
     topic_id: <telegramChatTopicId>

   groups:
     - name: 'group 1'
       keywords:
         - 'миска'
       include_keywords:
         - 'кот'
       exclude_keywords:
         - 'купить'
   ```

Configs keys descriptions:

- `chats` (only in config.dev.yaml for testing purposes): list of links where bot looks for donation messages. On the
  prod environment, donation chats list is returned from catebi API request.
- `sys_logging`: settings for bot logs, where `developers` - list of usernames to ping about some logs, `topic_id`-
  Telegram chat topic where bot sends logs to
- `groups`: a bunch of keywords on a specific sub-topic with filters, where `name` - group name, `keywords` - list of
  keywords about what we are looking for in donation messages, `include_keywords` - list of keywords that must be in a
  message to filter irrelevant occurrences of `keywords`, `exclude_keywords` - list of keywords that must NOT be in a
  donation message.

If a message contains both `include_keywords` and `exclude_keywords` entries, `exclude_keywords` entry has the highest
priority so this message must NOT be sent.

Important! Content in `include_keywords` and `exclude_keywords` should be in lemmatized form. You can get word
lemmatization form in `freegan_nlp.ipynb`. just insert text for lemmatization in cell with text variable:

```python
text = "продаю"
```   

And run all cells in notebook. Look for this cell:

```python
lemmatized_text = process_text(text)
lemmatized_text
```

This cell output shows the word lemmatization form. For instance:

```
'продавать'
```

