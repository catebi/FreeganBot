# FreeganBot
telegram bot to search for donations in chats and channels


## install guide

### prerequisites

1. **Python Installation**: The script is written in Python, so you need Python installed on your system. Python 3.6 or higher is recommended due to compatibility with the libraries used.

2. **Telethon Library**: Telethon is a Python library for interacting with Telegram's API. You can install it using pip:

   ```bash
   pip install telethon
   ```

3. **PyYAML Library**: PyYAML is used for parsing YAML files in Python. Install it using pip:

   ```bash
   pip install pyyaml
   ```

4. **Telegram API Credentials**: You need a Telegram API `api_id` and `api_hash`. These are obtained by registering your application on Telegram’s website. Here's how:

   - Go to [my.telegram.org](https://my.telegram.org).
   - Log in with your Telegram account.
   - Click on 'API development tools' and fill out the form to create a new application.
   - Once created, you'll receive your `api_id` and `api_hash`.

5. **Internet Connection**: Since the script interacts with Telegram's servers, an active internet connection is required.

6. **A Telegram Account**: The script will run under your Telegram account, so ensure you have access to the account you intend to use.

### additional description

- api_id и api_hash можно получить с сайта https://my.telegram.org (API development)
- При первом запуске потребуется ввести номер телефона, к которому привязан телеграмм аккаунт, или токен бота (получать через BotFather)
- Первый параметр TelegramClient – session, это имя сеанса (или полный путь). В каталоге или по переданному пути будет создан файл с информацией о сессии, чтобы в дальнейшем не вводить данные повторно (вообще данные пользователя(бота) можно будет прописать в коде).
- Пользователь или бот должен состоять в группе, откуда планируется пересылать сообщения. Первый параметр в send_message – чат (имя пользователя/ id/ номер из контактов/ точные названия), куда сообщения будут отправлены.

Что может сломаться:

- в библиотеке Chat (небольшой групповой чат (группа)) и Channel – разные понятия, и часть кода с ссылкой на сообщение работает только с Channel. В природе сложно встретить что-то, что не являлось бы каналом и вызывало бы ошибку, если не создавать маленькую закрытую группу и не отправлять самому себе сообщения. Всё, что имеет общедоступное имя пользователя, – уже канал.

## telegram flea markets

```text
https://t.me/baraholka_tbi
https://t.me/avito_baraholka_tbilisi
https://t.me/baraholka_tbilisi
https://t.me/otdam_tbilisi
https://t.me/tbilisi_obyavleniya
https://t.me/Tbilisi_help
https://t.me/freegantbilisi
https://t.me/Tbilisi_market_bg
https://t.me/rabbitsbaraholka
```

## keywords

```text
'бентонит'
'бетонит'
'веревка'
'габапентин'
'джут'
'джутовая'
'джутовый'
'домик'
'дралка'
'игрушки'
'клетка'
'коврик'
'когтедерка'
'когтедралка'
'когтеточка'
'консервы'
'корм'
'кот'
'кошачий'
'кошачье'
'кошачья'
'кошка'
'кошкам'
'кошке'
'лежак'
'лежанка'
'лекарства'
'лоток'
'мальт-паста'
'миска'
'миски'
'молоко'
'мята'
'наполнитель'
'паучи'
'паштет'
'пеленки'
'перевозка'
'переноска'
'поводок'
'подстилка'
'подушка'
'поилка'
'тоннель'
'точилка'
'туннель'
'фонтанчик'
'шлейка'
'шприцы'
```

## config for bot

```yaml

telegram_chats:
 - https://t.me/baraholka_tbi
 - https://t.me/avito_baraholka_tbilisi
 - https://t.me/baraholka_tbilisi
 - https://t.me/otdam_tbilisi
 - https://t.me/tbilisi_obyavleniya
 - https://t.me/Tbilisi_help
 - https://t.me/freegantbilisi
 - https://t.me/Tbilisi_market_bg
 - https://t.me/rabbitsbaraholka

keywords:
 - 'бентонит'
 - 'бетонит'
 - 'веревка'
 - 'габапентин'
 - 'джут'
 - 'джутовая'
 - 'джутовый'
 - 'домик'
 - 'дралка'
 - 'игрушки'
 - 'клетка'
 - 'коврик'
 - 'когтедерка'
 - 'когтедралка'
 - 'когтеточка'
 - 'консервы'
 - 'корм'
 - 'кот'
 - 'кошачий'
 - 'кошачье'
 - 'кошачья'
 - 'кошка'
 - 'кошкам'
 - 'кошке'
 - 'лежак'
 - 'лежанка'
 - 'лекарства'
 - 'лоток'
 - 'мальт-паста'
 - 'миска'
 - 'миски'
 - 'молоко'
 - 'мята'
 - 'наполнитель'
 - 'паучи'
 - 'паштет'
 - 'пеленки'
 - 'перевозка'
 - 'переноска'
 - 'поводок'
 - 'подстилка'
 - 'подушка'
 - 'поилка'
 - 'тоннель'
 - 'точилка'
 - 'туннель'
 - 'фонтанчик'
 - 'шлейка'
 - 'шприцы'
```