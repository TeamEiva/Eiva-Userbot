import asyncio
import requests
from telethon import functions
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

msg = f"""
**⚡ ʟɛɢɛռɖaʀʏ ᴀғ EIVABOT⚡**

  •        [📑 Repo 📑](https://github.com/TeamEivaBot/EivaBot)
  •        [🚀 Deploy 🚀](https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FTeamEivaBot%2FEivaBot&template=https%3A%2F%2Fgithub.com%2FTeamEivabot%2FEivabot)

  •  ©️ {Eiva_channel} ™
"""
botname = Config.BOT_USERNAME

@bot.on(Eiva_cmd(pattern="repo$"))
@bot.on(sudo_cmd(pattern="repo$", allow_sudo=True))
async def repo(event):
    try:
        Eiva = await bot.inline_query(botname, "repo")
        await Eiva[0].click(event.chat_id)
        if event.sender_id == Ryoishin:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


@bot.on(Eiva_cmd(pattern="help ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="help ?(.*)", allow_sudo=True))
async def yardim(event):
    if event.fwd_from:
        return
    tgbotusername = Config.BOT_USERNAME
    input_str = event.pattern_match.group(1)
    if input_str:
        if input_str in CMD_HELP:
            return await eor(event, str(CMD_HELP[input_str]))
        return await eor(event, f"No help entry found for `{input_str}`.")
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "Eivabot_help")
            if not results:
                return await eor(event, "The inline help bot returned no results.")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except Exception as exc:
            await eor(event, f"Could not open inline help: `{exc}`")
    else:
        await eor(event, "**⚠️ ERROR !!** \nPlease Re-Check BOT_TOKEN & BOT_USERNAME on Heroku.")


@bot.on(Eiva_cmd(pattern="plinfo(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="plinfo(?: |$)(.*)", allow_sudo=True))
async def Eivabott(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await eor(event, str(CMD_HELP[args]))
        else:
            await eod(event, "**⚠️ Error !** \nNeed a module name to show plugin info.")
    else:
        string = ""
        sayfa = [
            sorted(list(CMD_HELP))[i : i + 5]
            for i in range(0, len(sorted(list(CMD_HELP))), 5)
        ]

        for i in sayfa:
            string += f"`✘ `"
            for sira, a in enumerate(i):
                string += "`" + str(a)
                string += "`" if sira == i.index(i[-1]) else "`, "
            string += "\n"
        await eod(event, "Please Specify A Module Name Of Which You Want Info" + "\n\n" + string)

# Eivabot
