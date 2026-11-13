import os
import heroku3
from telethon.tl.functions.users import GetFullUserRequest

from . import *

Heroku = heroku3.from_key(Config.HEROKU_API_KEY) if Config.HEROKU_API_KEY else None
heroku_api = "https://api.heroku.com"
sudousers = os.environ.get("SUDO_USERS", None)


@bot.on(Eiva_cmd(pattern="sudo"))
async def sudo(event):
    sudo = "True" if Config.SUDO_USERS else "False"
    users = os.environ.get("SUDO_USERS", None)
    if sudo == "True":
        await eod(event, f"📍 **Sudo :**  `Enabled`\n\n📝 **Sudo users :**  `{users}`", 10)
    else:
        await eod(event, f"📍 **Sudo :**  `Disabled`", 7)


@bot.on(Eiva_cmd(pattern="addsudo(?: |$)"))
async def add(event):
    ok = await eor(event, "**🚀 Adding Sudo User...**")
    bot = "SUDO_USERS"
    if Heroku and Config.HEROKU_APP_NAME:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        await eod(ok, "**Please Set-Up**  `HEROKU_APP_NAME` **to add sudo users!!**")
        return
    heroku_Config = app.config()
    if event is None:
        return
    try:
        target = await get_user(event)
    except Exception:
        await eod(ok, f"Reply to a user to add them in sudo.")
        return
    newsudo = f"{sudousers} {target}" if sudousers else f"{target}"
    await ok.edit(f"✅** Added**  `{target}`  **in Sudo User.**\n\n __Restarting Heroku to Apply Changes. Wait for a minute.__")
    heroku_Config[bot] = newsudo

@bot.on(Eiva_cmd(pattern="rmsudo(?: |$)"))
async def _(event):
    ok = await eor(event, "**🚫 Removing Sudo User...**")
    if Heroku and Config.HEROKU_APP_NAME:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        await eod(ok, "**Please Set-Up**  HEROKU_APP_NAME to remove sudo users!!")
        return
    heroku_Config = app.config()
    if event is None:
        return
    try:
        target = await get_user(event)
        gett = str(target)
    except Exception:
        await eod(ok, f"Reply to a user to remove them from sudo.")
        return
    if gett in (sudousers or ""):
        newsudo = sudousers.replace(gett, "")
        await ok.edit(f"❌** Removed**  `{target}`  from Sudo User.\n\n Restarting Heroku to Apply Changes. Wait for a minute.")
        bot = "SUDO_USERS"
        heroku_Config[bot] = newsudo
    else:
        await ok.edit("**😑This user is not in your Sudo Users List.**")

async def get_user(event):
    if not event.reply_to_msg_id:
        raise ValueError("Reply to a user to select them")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_id = (
            previous_message.forward.sender_id
            if previous_message and previous_message.forward
            else previous_message.sender_id if previous_message else None
        )
        if user_id is None:
            raise ValueError("Could not identify the replied user")
        replied_user = await event.client(GetFullUserRequest(user_id))
    return replied_user.user.id


CmdHelp("sudo").add_command(
  "sudo", None, "Check If Your Bot Has Sudo Enabled!!"
).add_command(
  "addsudo", "<reply to user>", "Adds replied user to sudo list."
).add_command(
  "rmsudo", "<reply to user>", "Removes the replied user from your sudo list if already added."
).add_info(
  "Manage Sudo."
).add_warning(
  "⚠️ Grant Sudo Access to someone you trust!"
).add()
