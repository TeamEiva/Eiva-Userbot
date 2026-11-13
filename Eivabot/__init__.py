import os
import sys
import time
import datetime
from logging import DEBUG, INFO, basicConfig, getLogger

import heroku3
from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

from Eivabot.config import Config

StartTime = datetime.datetime.now()

CONSOLE_LOGGER_VERBOSE = os.environ.get("CONSOLE_LOGGER_VERBOSE", "false").strip().lower() in {"1", "true", "yes", "on"}

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)


try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


if Config.EivaBOT_SESSION:
    session_name = str(Config.EivaBOT_SESSION)
    try:
        bot = TelegramClient(
            StringSession(session_name),
            int(Config.APP_ID or 1),
            Config.API_HASH or "0" * 32,
        )
    except Exception:
        LOGS.error("EivaBOT_SESSION could not be initialized; verify the session and API credentials")
        sys.exit()
else:
    session_name = "startup"
    bot = TelegramClient(session_name, int(Config.APP_ID or 1), Config.API_HASH or "0" * 32)

tbot = TelegramClient('Eivabot', api_id=int(Config.APP_ID or 1), api_hash=Config.API_HASH or "0" * 32)


# global variables
CMD_LIST = {}
CMD_HELP = {}
CMD_HELP_BOT = {}
BRAIN_CHECKER = []
INT_PLUG = ""
LOAD_PLUG = {}
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
ISAFK = False
AFKREASON = None
SUDO_LIST = {}


# Eivabot
