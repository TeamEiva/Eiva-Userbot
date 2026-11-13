from asyncio import sleep
from telethon.errors import rpcbaseerrors

from . import *

lg_id = Config.LOGGER_ID


@bot.on(Eiva_cmd(pattern="del$"))
@bot.on(sudo_cmd(pattern="del$", allow_sudo=True))
@errors_handler
async def delete_it(safai):
    msg_src = await safai.get_reply_message()
    if safai.reply_to_msg_id:
        try:
            await msg_src.delete()
            await safai.delete()
        except rpcbaseerrors.BadRequestError:
        	pass


@bot.on(Eiva_cmd(pattern=r"purge", outgoing=True))
@bot.on(sudo_cmd(pattern=r"purge", allow_sudo=True))
@errors_handler
async def fastpurger(purg):
    if not purg.reply_to_msg_id:
        return await edit_or_reply(purg, "Reply to the first message to purge from.")
    chat = await purg.get_input_chat()
    msgs = []
    count = 0

    async for msg in purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id - 1):
        msgs.append(msg.id)
        count += 1
        if len(msgs) >= 100:
            await purg.client.delete_messages(chat, msgs)
            msgs = []

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        "**Fast Purge Completed!** \nPurged `" + str(count) + "` messages.",
    )

    if lg_id:
        await purg.client.send_message(lg_id, f"#PURGE\n\nPurged `{count}` messages.")
    await sleep(2)
    await done.delete()


@bot.on(Eiva_cmd(pattern=r"purgeme", outgoing=True))
@bot.on(sudo_cmd(pattern=r"purgeme", allow_sudo=True))
@errors_handler
async def purgeme(delme):
    message = delme.text
    try:
        count = int(message.split(maxsplit=1)[1])
    except (IndexError, ValueError):
        return await edit_or_reply(delme, "Usage: `purgeme <count>`")
    if count < 1 or count > 1000:
        return await edit_or_reply(delme, "Count must be between 1 and 1000.")
    i = 0

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i >= count + 1:
            break
        i += 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "**Self Purge Complete!** Purged  `" + str(count) + "`  messages.",
    )
    if lg_id:
        await delme.client.send_message(
            lg_id, "#PURGE \nSelf Purged  `" + str(count) + "`  messages."
        )
    await sleep(2)
    i = 1
    await smsg.delete()


@bot.on(Eiva_cmd(pattern=r"sd", outgoing=True))
@bot.on(sudo_cmd(pattern=r"sd", allow_sudo=True))
@errors_handler
async def selfdestruct(destroy):
    message = destroy.text
    try:
        _, seconds, text = message.split(maxsplit=2)
        counter = int(seconds)
    except (ValueError, IndexError):
        return await edit_or_reply(destroy, "Usage: `sd <seconds> <text>`")
    if counter < 1 or counter > 86400:
        return await edit_or_reply(destroy, "Delay must be between 1 and 86400 seconds.")
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    if lg_id:
        await destroy.client.send_message(lg_id, "#SELF_DESTRUCT\n\nSelf-destruct message completed.")
        

CmdHelp("purger").add_command(
  "purge", "<reply from a msg>", "Purges all the messages from replied message."
).add_command(
  "purgeme", "<no.of msgs>", "Purges the required number of your messages", "purgeme 100"
).add_command(
  "sd", "<time> <text>", "Sends a self destruct text. Fill time in secs", "sd 10 Eivao"
).add_command(
  "del", "<reply>", "Deletes the replied msg."
).add_info(
  "Ninja Techniques"
).add_warning(
  "✅ Harmless Module."
).add()
