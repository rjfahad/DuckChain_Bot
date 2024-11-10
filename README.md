![banner](https://i.ibb.co/n73mHPL/image.png)

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/DuckChain_bot/quack?startapp=KvNYn05S)
[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/CryptoBotScript)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=Python&logoColor=white)](https://www.python.org/downloads/release/python-3100/)

## Recommendation before use DuckChain Script.

# 🦆 AUTO FARM FOR DUCKCHAIN

![demo](https://i.ibb.co/fXMSWGN/image.png)

> [!WARNING]
> I am not responsible for your account. Please consider the potential risks before using this bot.

### Subscribe [Telegram](https://telegram.me/CryptoBotScript) 🔗
### Thanks to [GravelFire](https://github.com/GravelFire) for the code base 🚀

## Recommendation before use

# 🔥🔥 PYTHON version must be 3.10 🔥🔥

## Features  
| Feature                                                   | Supported |
|-----------------------------------------------------------|:---------:|
| Multithreading                                            |     ✅     |
| Proxy binding to session                                  |     ✅     |
| User-Agent binding to session                             |     ✅     |
| Support pyrogram .session                                 |     ✅     |
| Registration in bot                                       |     ✅     |
| Auto-tasks                                                |     ✅     |
| Auto-Tap                                                  |     ✅     |
| Daily rewards                                             |     ✅     |



## [Settings]
| Settings                |                                 Description                                 |
|-------------------------|:---------------------------------------------------------------------------:|
| **API_ID / API_HASH**   | Platform data from which to run the Telegram session (by default - android) |
| **REF_ID**              |                      Thing that goes after startapp=                        |
| **SUPPORT_AUTHOR**      | It will choose random refer id between yours & author  (by default - True)  |
| **OPEN_BOX**            |                      Auto Open Boxes (default - True)                       |
| **AUTO_TASK**           |                         Auto tasks (default - True)                         |
| **AUTO_QUACK**          |                       Auto Quack Duck (default - True)                      |
| **TOTAL_QUACK**         |                      How many Quack (by default - [1, 5])                   |
| **QUACK_DELAY**         |                 Sleep time between Quacks (by default - [0, 1])             |
| **START_DELAY**         |            Delay between sessions at start (by default - [5, 25])           |
| **FAKE_USERAGENT**      |          Use random fake useragent in session (default - True)              |
| **SLEEP_TIME**          |           Sleep time between cycles (by default - [7200, 10800])            |
| **USE_PROXY_FROM_FILE** |             Use provided proxies in session (default - True)                |


## Quick Start 📚

To fast install libraries and run bot - open run.bat on Windows or run.sh on Linux

## Prerequisites
Before you begin, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) **version 3.10**

## Obtaining API Keys
1. Go to my.telegram.org and log in using your phone number.
2. Select "API development tools" and fill out the form to register a new application.
3. Record the API_ID and API_HASH provided after registering your application in the .env file.

## Installation
You can download the [**repository**](https://github.com/outputman/DuckChain_Bot) by cloning it to your system and installing the necessary dependencies:
```shell
git clone https://github.com/outputman/DuckChain_Bot
```

Then you can do automatic installation by typing:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux manual installation
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

# 1 - Run clicker
# 2 - Creates a session
```

# Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```

# 1 - Run clicker
# 2 - Creates a session
```

### Usages
When you first launch the bot, create a session for it using the 'Creates a session' command. It will create a 'sessions' folder in which all accounts will be stored, as well as a file accounts.json with configurations.
If you already have sessions, simply place them in a folder 'sessions' and run the clicker. During the startup process you will be able to configure the use of a proxy for each session.
User-Agent is created automatically for each account.
