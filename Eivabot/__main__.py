"""Application entry point."""
import glob
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from Eivabot import LOGS, bot, tbot
from Eivabot.config import Config
from Eivabot.utils import load_module, start_assistant
from Eivabot.version import __Eiva__


def validate_config():
    required = ("APP_ID", "API_HASH", "EivaBOT_SESSION", "BOT_TOKEN")
    missing = [key for key in required if not getattr(Config, key, None)]
    if missing:
        raise SystemExit("Missing required configuration: " + ", ".join(missing))
    try:
        int(Config.APP_ID)
    except (TypeError, ValueError) as exc:
        raise SystemExit("APP_ID must be an integer") from exc


def load_plugins():
    for filename in sorted(glob.glob("Eivabot/plugins/*.py")):
        module_name = Path(filename).stem
        try:
            load_module(module_name)
        except Exception:
            LOGS.exception("Plugin %s failed to load", module_name)


def load_assistants():
    for filename in sorted(glob.glob("Eivabot/assistant/*.py")):
        module_name = Path(filename).stem
        try:
            start_assistant(module_name)
        except Exception:
            LOGS.exception("Assistant module %s failed to load", module_name)


async def announce_startup():
    if Config.LOGGER_ID:
        picture = Config.ALIVE_PIC or "https://telegra.ph/file/5501c52fed1b2229ad03d.jpg"
        try:
            await bot.send_file(
                Config.LOGGER_ID,
                picture,
                caption=f"#START\n\nEivaBot {__Eiva__} is online. Type `{Config.HANDLER}ping` or `{Config.HANDLER}alive` to check.",
            )
        except Exception:
            LOGS.exception("Could not send startup notification")
    try:
        await bot(JoinChannelRequest("@TheEiva"))
    except Exception:
        LOGS.debug("Could not join the update channel", exc_info=True)


def main():
    validate_config()
    bot.tgbot = None
    try:
        bot.start()
        bot.me = bot.loop.run_until_complete(bot.get_me())
        bot.uid = telethon.utils.get_peer_id(bot.me)
        tbot.start(bot_token=Config.BOT_TOKEN)
        bot.tgbot = tbot
    except Exception:
        LOGS.exception("Telegram startup failed")
        raise SystemExit(1)

    load_plugins()
    load_assistants()
    bot.loop.create_task(announce_startup())
    LOGS.info("EivaBot is running")
    try:
        bot.run_until_disconnected()
    finally:
        bot.loop.run_until_complete(bot.disconnect())
        if bot.tgbot:
            bot.loop.run_until_complete(bot.tgbot.disconnect())


if __name__ == "__main__":
    main()
