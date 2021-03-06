from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

#-------------------------------------------------------------------------------

Eiva_pic = Config.ALIVE_PIC or "https://telegra.ph/file/983d8452ac533a8c8d678.jpg"


apic=f"""
πΈππ£π π’π πππππ‘...

  πππ π‘ππ, πΌ'π ππππ£π.

 ββββββββββββββββββββββ
 β£ ππ€πππ - {Eiva_mention}
 β£ ππππ πππ - {Eiva_ver}
 β£ πππππ‘ππ  - ππ πππππ‘π
 β£ ππππππ -`{uptime}`
 β£ ππ¦π‘πππ - 3.9.5
 β£ πππππ‘πππ - `{tel_ver}`
 β£  π΅πππππ - ππππ 
 ββββββββββββββββββββββ
"""
#-------------------------------------------------------------------------------

@bot.on(Eiva_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def up(Eiva):
    if Eiva.fwd_from:
        return
    await Eiva.get_chat()
    await bot.send_file(Eiva.chat_id, Eiva_pic, caption=apic)
    await Eiva.delete()

msg = f"""
**β‘ πππ©πππ’π§ ππ¦ π’π‘πππ‘π β‘ **
{Config.ALIVE_MSG}
**π ππ’π§ π¦π§ππ§π¨π¦ π**
**π§ππππ§ππ’π‘:**  `{tel_ver}`
**πππ©πππ’π§  :**  **{Eiva_ver}**
**π¨π£π§ππ π   :**  `{uptime}`
**πππ¨π¦π    :**  **{abuse_m}**
**π¦π¨ππ’     :**  **{is_sudo}**
"""
botname = Config.BOT_USERNAME

@bot.on(Eiva_cmd(pattern="Eiva$"))
@bot.on(sudo_cmd(pattern="Eiva$", allow_sudo=True))
async def Eiva_a(event):
    try:
        Eiva = await bot.inline_query(botname, "alive")
        await Eiva[0].click(event.chat_id)
        if event.sender_id == Ryoishin:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "Eiva", None, "Shows Inline Alive Menu with more details."
).add_warning(
  "β Harmless Module"
).add()
