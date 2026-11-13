import asyncio
import logging

from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError, FloodWaitError
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest

from . import *

logger = logging.getLogger(__name__)


BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

@bot.on(Eiva_cmd(pattern=r"kickall ?(.*)"))
@bot.on(sudo_cmd(pattern=r"kickall ?(.*)", allow_sudo=True))
async def _(event):
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    rights = getattr(result.participant, "admin_rights", None)
    if not rights or not rights.ban_users:
        return await eod(
            event, "No immunity for this action!!"
        )
    Eiva = await eor(event, "**Bleck Magik Started...**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await asyncio.sleep(0.5)
        except Exception as e:
            logger.warning("Could not kick participant %s: %s", user.id, e)
            await asyncio.sleep(0.5)
    await Eiva.edit(
        "**Bleck Magik Done...**"
    )
    if Config.LOGGER_ID:
        await bot.send_message(
            Config.LOGGER_ID,
            f"#KICKALL \n\nKicked Out  `{success}`  of  `{total}`  members"
        )


@bot.on(Eiva_cmd(pattern=r"banall ?(.*)"))
@bot.on(sudo_cmd(pattern=r"banall ?(.*)", allow_sudo=True))
async def _(event):
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    rights = getattr(result.participant, "admin_rights", None)
    if not rights or not rights.ban_users:
        return await eod(
            event, "Immunity Low!!"
        )
    Eiva = await eor(event, "**Bleck Magik Begins..**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await asyncio.sleep(0.5)
        except Exception as e:
            logger.warning("Could not ban participant %s: %s", user.id, e)
            await asyncio.sleep(0.5)
    await Eiva.edit(
        "**Bleck Magik Completed...**"
    )
    if Config.LOGGER_ID:
        await bot.send_message(
            Config.LOGGER_ID,
            f"#BANALL \n\nSuccessfully banned  `{success}`  out of  `{total}`  members!!",
        )
    

@bot.on(Eiva_cmd(pattern=r"unbanall ?(.*)"))
@bot.on(sudo_cmd(pattern=r"unbanall ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            user = await event.client.get_entity(input_str.strip())
            await event.client(
                EditBannedRequest(
                    event.chat_id,
                    user,
                    ChatBannedRights(until_date=None, view_messages=False),
                )
            )
        except Exception as exc:
            return await edit_or_reply(event, f"Could not unban `{input_str}`: {exc}")
        return await edit_or_reply(event, f"Unbanned `{user.id}`.")

    if event.is_private:
        return await edit_or_reply(event, "Use this command in a group or channel.")
    chat = await event.get_chat()
    if not (chat.creator or (chat.admin_rights and chat.admin_rights.ban_users)):
        return await edit_or_reply(event, "I need ban rights to unban participants.")
    status = await edit_or_reply(event, "Searching the banned participant list...")
    count = 0
    async for user in event.client.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        rights = ChatBannedRights(until_date=None, view_messages=False)
        try:
            await event.client(EditBannedRequest(event.chat_id, user, rights))
            count += 1
        except FloodWaitError as exc:
            await asyncio.sleep(exc.seconds)
            await event.client(EditBannedRequest(event.chat_id, user, rights))
            count += 1
        except Exception as exc:
            logger.warning("Could not unban participant %s: %s", user.id, exc)
    await edit_or_reply(status, f"Unbanned {count} participant(s).")


@bot.on(Eiva_cmd(pattern="ikuck ?(.*)"))
@bot.on(sudo_cmd(pattern="ikuck ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await eod(event, "`You aren't an admin here!`")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    Eiva = await edit_or_reply(event, "Searching Participant Lists.")
    async for i in bot.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(Eiva, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(Eiva, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                else:
                    c += 1
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}"""
        await Eiva.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await asyncio.sleep(5)
    await Eiva.edit(
        """Total: {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )


async def ban_user(chat_id, i, rights):
    try:
        await bot(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


CmdHelp("banall").add_command(
  "ikuck", None, "Gives the data of group. Deleted accounts, Last seen, Offline, Online, Recently, Bots, Etc."
).add_command(
  "unbanall", None, "Unbans all the user in the chat."
).add_command(
  "banall", None, "Bans all the user in the chat.."
).add_command(
  "kickall", None, "Kicks all the users in the chat..."
).add_info(
  "⚠️ Group Destroyer"
).add_warning(
  "✅ Harmless Module."
).add()
