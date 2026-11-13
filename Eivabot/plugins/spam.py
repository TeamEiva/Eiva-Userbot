"""Rate-limited repeat-message commands."""
import asyncio

from . import *

_MAX_REPEAT = min(max(int(getattr(Config, "MAX_SPAM", 3)), 1), 10)


def parse_count_and_text(value):
    try:
        count_text, text = value.strip().split(maxsplit=1)
        count = int(count_text)
    except (ValueError, TypeError):
        raise ValueError("Usage: `<count> <message>`") from None
    if count < 1 or count > _MAX_REPEAT:
        raise ValueError(f"Count must be between 1 and {_MAX_REPEAT}.")
    if not text.strip():
        raise ValueError("Message cannot be empty.")
    return count, text.strip()


async def repeat(event, count, text, delay=0):
    for index in range(count):
        await event.respond(text)
        if delay and index + 1 < count:
            await asyncio.sleep(delay)
    if event.out:
        await event.delete()
    if Config.LOGGER_ID:
        await event.client.send_message(
            Config.LOGGER_ID, f"#REPEAT\n\nSent {count} message(s)."
        )


@bot.on(Eiva_cmd(pattern=r"spam\s+(.+)"))
@bot.on(sudo_cmd(pattern=r"spam\s+(.+)", allow_sudo=True))
async def spammer(event):
    if event.fwd_from:
        return
    try:
        count, text = parse_count_and_text(event.pattern_match.group(1))
        await repeat(event, count, text)
    except ValueError as exc:
        await edit_or_reply(event, str(exc))


@bot.on(Eiva_cmd(pattern=r"bigspam\s+(.+)"))
@bot.on(sudo_cmd(pattern=r"bigspam\s+(.+)", allow_sudo=True))
async def bigspam(event):
    await spammer(event)


@bot.on(Eiva_cmd(pattern=r"dspam\s+(.+)"))
@bot.on(sudo_cmd(pattern=r"dspam\s+(.+)", allow_sudo=True))
async def delayed_spam(event):
    try:
        delay_text, count_text, text = event.pattern_match.group(1).strip().split(maxsplit=2)
        delay = float(delay_text)
        count, text = parse_count_and_text(f"{count_text} {text}")
        if not 1 <= delay <= 60:
            raise ValueError("Delay must be between 1 and 60 seconds.")
        await repeat(event, count, text, delay)
    except (ValueError, TypeError) as exc:
        await edit_or_reply(event, f"Invalid arguments: {exc}")


@bot.on(Eiva_cmd(pattern=r"uspam(?:\s+.*)?$"))
@bot.on(sudo_cmd(pattern=r"uspam(?:\s+.*)?$", allow_sudo=True))
async def unlimited_spam(event):
    await edit_or_reply(event, "Unlimited repetition is disabled. Use `spam <count> <message>` (maximum 3 by default).")


@bot.on(Eiva_cmd(pattern=r"bspam\s+(.+)"))
@bot.on(sudo_cmd(pattern=r"bspam\s+(.+)", allow_sudo=True))
async def break_spam(event):
    await spammer(event)


@bot.on(Eiva_cmd(pattern=r"mspam\s+(\d+)"))
@bot.on(sudo_cmd(pattern=r"mspam\s+(\d+)", allow_sudo=True))
async def media_spam(event):
    try:
        count = int(event.pattern_match.group(1))
        if not 1 <= count <= _MAX_REPEAT:
            raise ValueError(f"Count must be between 1 and {_MAX_REPEAT}.")
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            raise ValueError("Reply to a media message.")
        for _ in range(count):
            await event.client.send_file(event.chat_id, reply.media)
        if event.out:
            await event.delete()
    except ValueError as exc:
        await edit_or_reply(event, str(exc))


CmdHelp("spam").add_command(
    "spam", "<count> <message>", f"Repeat a message up to {_MAX_REPEAT} times."
).add_command(
    "dspam", "<delay> <count> <message>", "Repeat with a 1–60 second delay."
).add_command(
    "mspam", "<count> (reply to media)", f"Repeat replied media up to {_MAX_REPEAT} times."
).add_command(
    "uspam", None, "Unlimited repetition is disabled; use the bounded spam command."
).add_info("Rate-limited repeat commands").add()
