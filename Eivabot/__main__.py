import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest

from Eivabot import LOGS, bot, tbot
from Eivabot.config import Config
from Eivabot.utils import load_module, start_assistant
from Eivabot.version import __Eiva__ as Eivaver
hl = Config.HANDLER
Eiva_PIC = Config.ALIVE_PIC or "https://telegra.ph/file/5501c52fed1b2229ad03d.jpg"

# let's get the bot ready
async def Eiva_bot(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"EivaBOT_SESSION - {str(e)}")
        sys.exit()


# Eivabot starter...
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = TelegramClient(
                "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
            ).start(bot_token=Config.BOT_TOKEN)
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("🔰 Starting EivaBot 🔰")
            bot.loop.run_until_complete(Eiva_bot(Config.BOT_USERNAME))
            LOGS.info("🔥 EivaBot Startup Completed 🔥")
        else:
            bot.start()
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()

# imports plugins...
path = "Eivabot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))

async def asst():
  """
  Loading Assistant From here
  """
  path = 'Eivabot/assistant/*.py'
  files = glob.glob(path)
  for name in files:
    with open(name) as f:
      path1 = Path(f.name)
      shortname = path1.stem
      start_assistant(shortname.replace(".py", ""))

# Extra Modules...
# extra_repo = Config.EXTRA_REPO or "https://github.com/TeamEiva/Extra"
# if Config.EXTRA == "True":
#    try:
#       os.system(f"git clone {extra_repo}")
#    except BaseException:
#        pass
#   LOGS.info("Installing Extra Plugins")
#    path = "hellbot/plugins/*.py"
#   files = glob.glob(path)
#    for name in files:
#        with open(name) as ex:
#            path2 = Path(ex.name)
#            shortname = path2.stem
#            load_module(shortname.replace(".py", ""))


# let the party begin...
LOGS.info("Starting Bot Mode !")
tbot.start()
LOGS.info("⚡ Your EivaBot Is Now Working ⚡")
LOGS.info(
    "Head to @TheEiva for Updates. Also join chat group to get help regarding to EivaBot."
)

# that's life...
async def Eiva_is_on():
    try:
        if Config.LOGGER_ID != 0:
            await bot.send_file(
                Config.LOGGER_ID,
                Eiva_PIC,
                caption=f"#START \n\nDeployed ΣIVΛBθƬ Successfully\n\n**ΣIVΛBθƬ - {Eivaver}**\n\nType `{hl}ping` or `{hl}alive` to check! \n\nJoin [ΣIVΛBθƬ Channel](t.me/TheEiva) for Updates & [ΣIVΛBθƬ Chat](t.me/EivaSupport) for any query regarding ΣIVΛBθƬ",
            )
    except Exception as e:
        LOGS.info(str(e))

# Join EivaBot Channel after deploying 🤐😅
    try:
        await bot(JoinChannelRequest("@TheEiva"))
    except BaseException:
        pass

# Why not come here and chat??
#    try:
#        await bot(JoinChannelRequest("@EivaSupport"))
#    except BaseException:
 #       pass



bot.loop.create_task(Eiva_is_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()

# Eivabot
