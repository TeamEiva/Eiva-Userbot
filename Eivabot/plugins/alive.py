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
𝐸𝑖𝑣𝑎 𝑢𝑠𝑒𝑟𝑏𝑜𝑡...

  𝑀𝑎𝑠𝑡𝑒𝑟, 𝐼'𝑚 𝑎𝑙𝑖𝑣𝑒.

 ┏━━━━━━━━━━━━━━━━━━━━━
 ┣ 𝑂𝑤𝑛𝑒𝑟 - {Eiva_mention}
 ┣ 𝑉𝑒𝑟𝑠𝑖𝑜𝑛 - {Eiva_ver}
 ┣ 𝑈𝑝𝑑𝑎𝑡𝑒𝑠 - 𝑁𝑜 𝑈𝑝𝑑𝑎𝑡𝑒
 ┣ 𝑈𝑝𝑇𝑖𝑚𝑒 - 1𝒉:2𝑚:46𝑠
 ┣ 𝑃𝑦𝑡𝒉𝑜𝑛 - 3.9.5
 ┣ 𝑇𝑒𝑙𝑒𝑡𝒉𝑜𝑛 - `{tel_ver}`
 ┣  𝐵𝑟𝑎𝑛𝑐𝒉 - 𝑀𝑎𝑖𝑛 
 ┗━━━━━━━━━━━━━━━━━━━━━
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
**⚡ 𝗘𝗜𝗩𝗔𝗕𝗢𝗧 𝗜𝗦 𝗢𝗡𝗟𝗜𝗡𝗘 ⚡ **
{Config.ALIVE_MSG}
**🏅 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦 🏅**
**𝗧𝗘𝗟𝗘𝗧𝗛𝗢𝗡:**  `{tel_ver}`
**𝗘𝗜𝗩𝗔𝗕𝗢𝗧  :**  **{Eiva_ver}**
**𝗨𝗣𝗧𝗜𝗠𝗘   :**  `{uptime}`
**𝗔𝗕𝗨𝗦𝗘    :**  **{abuse_m}**
**𝗦𝗨𝗗𝗢     :**  **{is_sudo}**
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
