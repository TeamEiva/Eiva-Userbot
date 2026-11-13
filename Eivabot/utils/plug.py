import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from Eivabot import *
from Eivabot.helpers import *
from Eivabot.config import *
from Eivabot.utils import *


# ENV
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from Eivabot.config import Config
elif os.path.exists("Config.py"):
    from Config import Development as Config


# load plugins
def load_module(shortname):
    if shortname.startswith("__"):
        return

    import Eivabot.utils

    path = Path(f"Eivabot/plugins/{shortname}.py")
    name = f"Eivabot.plugins.{shortname}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create an import spec for plugin {shortname}")
    mod = importlib.util.module_from_spec(spec)
    mod.bot = bot
    mod.tgbot = bot.tgbot
    mod.command = command
    mod.logger = logging.getLogger(shortname)
    mod.Config = Config
    mod.borg = bot
    mod.Eivabot = bot
    mod.edit_or_reply = edit_or_reply
    mod.eor = edit_or_reply
    mod.delete_Eiva = delete_Eiva
    mod.eod = delete_Eiva
    mod.Var = Config
    mod.admin_cmd = Eiva_cmd

    # Compatibility aliases used by older plugins.
    sys.modules["uniborg.util"] = Eivabot.utils
    sys.modules["userbot.utils"] = Eivabot.utils
    sys.modules["userbot"] = Eivabot
    sys.modules["userbot.events"] = Eivabot
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        for index in reversed(range(len(bot._event_builders))):
            _, callback = bot._event_builders[index]
            if getattr(callback, "__module__", None) == name:
                del bot._event_builders[index]
        raise
    LOGS.info("Successfully imported plugin %s", shortname)


# remove plugins
def remove_plugin(shortname):
    name = f"Eivabot.plugins.{shortname}"
    removed = False
    for client in (bot, getattr(bot, "tgbot", None)):
        if client is None:
            continue
        for index in reversed(range(len(client._event_builders))):
            _, callback = client._event_builders[index]
            if getattr(callback, "__module__", None) == name:
                del client._event_builders[index]
                removed = True
    LOAD_PLUG.pop(shortname, None)
    sys.modules.pop(name, None)
    return removed

# Eivabot
