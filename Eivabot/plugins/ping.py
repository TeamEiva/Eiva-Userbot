import asyncio
import datetime

from . import *

@bot.on(Eiva_cmd(pattern="ping$"))
@bot.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def pong(Eiva):
    if Eiva.fwd_from:
        return
    start = datetime.datetime.now()
    event = await eor(Eiva, "`·.·★ ℘ıŋɠ ★·.·´")
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(
        f"༒  ρσиg ༒\n\n    💫  `{ms}`\n    💫  __**Oɯɳҽɾ**__ **:**  {Eiva_mention}"
    )


CmdHelp("ping").add_command(
  "ping", None, "Checks the ping speed of your ΣIVΛBθƬ"
).add_warning(
  "✅ Harmless Module"
).add()

# Eivabot
