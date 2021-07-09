from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

#-------------------------------------------------------------------------------

Eiva_pic = Config.ALIVE_PIC or "https://telegra.ph/file/cca0cd6ee5e1939ebf1c9.jpg"
alive_c = f"__**🔥🔥єιναϐοτ ιѕ οиℓιиє🔥🔥**__\n\n"
alive_c += f"__↼ Oɯɳҽɾ ⇀__ : 『 {Eiva_mention} 』\n\n"
alive_c += f"•♦• Tҽʅҽƚԋσɳ    :  `{tel_ver}` \n"
alive_c += f"•♦• EιʋαVҽɾʂισɳ      :  __**{Eiva_ver}**__\n"
alive_c += f"•♦• Sυԃσ           :  `{is_sudo}`\n"
alive_c += f"•♦• Cԋαɳɳҽʅ     :  {Eiva_channel}\n"

#-------------------------------------------------------------------------------

@bot.on(Eiva_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def up(Eiva):
    if Eiva.fwd_from:
        return
    await Eiva.get_chat()
    await Eiva.delete()
    await bot.send_file(Eiva.chat_id, Eiva_pic, caption=alive_c)
    await Eiva.delete()

msg = f"""
**⚡ ΣIVΛBθƬ IS θПLIПΣ ⚡ **
{Config.ALIVE_MSG}
**🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅**
**Telethon :**  `{tel_ver}`
**ΣIVΛBθƬ  :**  **{Eiva_ver}**
**Uptime   :**  `{uptime}`
**Abuse    :**  **{abuse_m}**
**Sudo      :**  **{is_sudo}**
"""
botname = Config.BOT_USERNAME

@bot.on(Eiva_cmd(pattern="Eiva$"))
@bot.on(sudo_cmd(pattern="Eiva$", allow_sudo=True))
async def Eiva_a(event):
    try:
        Eiva = await bot.inline_query(botname, "alive")
        await Eiva[0].click(event.chat_id)
        if event.sender_id == ForGo10God:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "Eiva", None, "Shows Inline Alive Menu with more details."
).add_warning(
  "✅ Harmless Module"
).add()
