# FreeganBot
Telegram bot to search for donations in chats and channels

## Install guide

### Prerequisites

1. **Python Installation**: The script is written in Python, so you need Python installed on your system. Python 3.6 or higher is recommended due to compatibility with the libraries used.

2. **Setting Up Venv**: First, create [venv](https://docs.python.org/3/library/venv.html) for the project with this command:
   ```bash
   python -m venv venv
   ```
   Next, activate venv:
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**: install all required dependencies with this [command](https://pip.pypa.io/en/stable/user_guide/):

   ```bash
   pip install -r requirements.txt
   ```

4. **Telegram API Credentials**: You need a Telegram API `api_id` and `api_hash`. These are obtained by registering your application on Telegram’s website. Here's how:

   - Go to [my.telegram.org](https://my.telegram.org).
   - Log in with your Telegram account.
   - Click on 'API development tools' and fill out the form to create a new application.
   - Once created, you'll receive your `api_id` and `api_hash`.

5. **Internet Connection**: Since the script interacts with Telegram's servers, an active internet connection is required.

6. **A Telegram Account**: The script will run under your Telegram account, so ensure you have access to the account you intend to use.

7. **Environment Variables**: copy `env.example` content into `.env` file with this command:
   ```bash
   [ ! -f .env ] && cp env.example .env
   ```
   And insert these variables into your `.env` file:

   - `ENV` is prod/dev (dev is default).
   - `TELEGRAM_API_ID` is from [my.telegram.org](https://my.telegram.org) `api_id`.
   - `TELEGRAM_API_HASH` is from [my.telegram.org](https://my.telegram.org) `api_hash`.
   - `TELEGRAM_CHAT_SEND_TO` is Telegram Username where bot should send donation messages to (for dev purposes it's usually your test chat).

8. **Setting up your test environment**: You should test the bot functions with your test chat. Here's how to do that:

   - Create a public chat or channel in Telegram
   - Add [@freegan_catebi_leshiy_bot](https://t.me/freegan_catebi_leshiy_bot) into your chat
   - Give it Admin role and make sure bot is allowed to send messages in the chat

   
### Additional Description

- At the first launch, in the terminal you will need to enter the phone number to which your Telegram account is linked
- You can read about TelegramClient methods [here](https://docs.telethon.dev/en/stable/modules/client.html)
- When the program runs, it creates `catebi_freegan.session` file with information about the session, so that in the future do not re-enter the data (in general, user (bot) data can be written in the code)

### Troubleshooting

- in the Chat library - a small group chat (group) - and Channel are different concepts, and the message reference part of the code only works with Channel. It's hard to encounter anything in nature that isn't a channel and causes an error unless you create a small closed group and send messages to yourself. Anything with a public username is already a channel.
- The user or bot must be a member of the group from which it is planned to send messages.

## Bot Config

- `chats` (only in config.dev.yaml for testing purposes): list of links where bot looks for donation messages. On the prod environment, donation chats list is returned from catebi API request.
- `sys_logging`: settings for bot logs, where `developers` - list of usernames to ping about some logs, `topic_id`- Telegram chat topic where bot sends logs to
- `groups`: a bunch of keywords on a specific sub-topic with filters, where `name` - group name, `keywords` - list of keywords about what we are looking for in donation messages, `include_keywords` - list of keywords that must be in a message to filter irrelevant occurrences of `keywords`, `exclude_keywords` - list of keywords that must NOT be in a donation message. If a message contains both `include_keywords` and `exclude_keywords` entries, `exclude_keywords` entry has the highest priority so this message must NOT be sent

```yaml
chats:                         # only for dev environment
  - https://t.me/catebitest01  # for testing purposes
  - https://t.me/catebitest02  # for testing purposes

sys_logging:
  developers:  "@lejafo"
  topic_id: 2693
 
groups:
  - name: 'main group'
    keywords:
      - 'ампула'
      - 'бентонит'
      - 'бетонит'
      - 'верёвка'
      - 'вольер'
      - 'габа'
      - 'габапентин'
      - 'джут'
      - 'джутовый'
      - 'дралка'
      - 'инъекция'
      - 'когтедерка'
      - 'когтедралка'
      - 'когтеточка'
      - 'консервы'
      - 'корм'
      - 'кот'
      - 'кошачий'
      - 'кошка'
      - 'лежак'
      - 'лежанка'
      - 'лотков'
      - 'лоток'
      - 'мальтпаста'
      - 'мальт-паста'
      - 'молоко'
      - 'паучить'
      - 'паштет'
      - 'пелёнка'
      - 'поводок'
      - 'подстилка'
      - 'подушечка'
      - 'поилка'
      - 'тоннель'
      - 'точилка'
      - 'туннель'
      - 'укол'
      - 'фонтанчик'
      - 'шлейка'
      - 'шприц'
    include_keywords:
      - 'животное'
      - 'кошачий'
      - 'кошка'
      - 'кот'
  - name: 'air conditioner group'
    keywords:
      - 'кондиционер'
      - 'кондей'
      - 'сплитсистема'
      - 'сплит-система'
    exclude_keywords:
      - 'аренда'
      - 'купить'
      - 'шампунь'
      - 'сдаваться'
      - 'сдавать'
      - 'сдать'
      - 'трансфер'
      - 'визаран'
```
