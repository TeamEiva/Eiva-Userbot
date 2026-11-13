"""Safe file management for the bot's work directories."""
import io
from pathlib import Path

from . import *

ROOT = Path.cwd().resolve()
SAVED_DIR = (ROOT / "SAVED").resolve()
DOWNLOAD_DIR = Path(Config.TMP_DOWNLOAD_DIRECTORY).resolve()
SAVED_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _within(path, base):
    resolved = (base / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    if resolved != base and base not in resolved.parents:
        raise ValueError("Path must stay inside the allowed directory")
    return resolved


async def _send_listing(event, title, entries):
    text = title + "\n" + "\n".join(f"• `{entry}`" for entry in entries)
    if len(text) <= Config.MAX_MESSAGE_SIZE_LIMIT:
        return await edit_or_reply(event, text or f"{title}\n(empty)")
    payload = io.BytesIO(text.encode("utf-8"))
    payload.name = "files.txt"
    return await event.client.send_file(
        event.chat_id, payload, force_document=True, caption=title
    )


@bot.on(Eiva_cmd(pattern=r"ls(?:\s+(.+))?$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"ls(?:\s+(.+))?$", allow_sudo=True))
async def list_path(event):
    target = event.pattern_match.group(1)
    try:
        directory = _within(target.strip(), ROOT) if target else ROOT
        if not directory.is_dir():
            raise ValueError("Path is not a directory")
        await _send_listing(event, f"Files in `{directory.relative_to(ROOT) or '.'}`:", sorted(p.name for p in directory.iterdir()))
    except (OSError, ValueError) as exc:
        await edit_or_reply(event, f"Cannot list path: `{exc}`")


async def _list_fixed(event, directory, label):
    try:
        entries = sorted(path.name for path in directory.iterdir())
        await _send_listing(event, label, entries)
    except OSError as exc:
        await edit_or_reply(event, f"Cannot list files: `{exc}`")


@bot.on(Eiva_cmd(pattern=r"ls_local$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"ls_local$", allow_sudo=True))
async def list_downloads(event):
    await _list_fixed(event, DOWNLOAD_DIR, "Downloaded media:")


@bot.on(Eiva_cmd(pattern=r"ls_root$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"ls_root$", allow_sudo=True))
async def list_root(event):
    await _list_fixed(event, ROOT, "Repository files:")


@bot.on(Eiva_cmd(pattern=r"ls_saved$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"ls_saved$", allow_sudo=True))
async def list_saved(event):
    await _list_fixed(event, SAVED_DIR, "Saved files:")


async def _rename(event, raw, base):
    try:
        source, destination = (part.strip() for part in raw.split("|", 1))
        if not source or not destination:
            raise ValueError("Provide both names separated by `|`.")
        src = _within(source, base)
        dst = _within(destination, base)
        if not src.is_file():
            raise ValueError("Source file does not exist")
        if dst.exists():
            raise ValueError("Destination already exists")
        src.rename(dst)
        await edit_or_reply(event, f"Renamed `{src.name}` to `{dst.name}`")
    except (OSError, ValueError) as exc:
        await edit_or_reply(event, f"Rename failed: `{exc}`")


@bot.on(Eiva_cmd(pattern=r"rnsaved\s+(.+)$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"rnsaved\s+(.+)$", allow_sudo=True))
async def rename_saved(event):
    await _rename(event, event.pattern_match.group(1), SAVED_DIR)


@bot.on(Eiva_cmd(pattern=r"rnlocal\s+(.+)$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"rnlocal\s+(.+)$", allow_sudo=True))
async def rename_download(event):
    await _rename(event, event.pattern_match.group(1), DOWNLOAD_DIR)


async def _delete_file(event, raw, base):
    try:
        path = _within(raw.strip(), base)
        if not path.is_file():
            raise ValueError("File does not exist")
        path.unlink()
        await edit_or_reply(event, f"Deleted `{path.name}`")
    except (OSError, ValueError) as exc:
        await edit_or_reply(event, f"Delete failed: `{exc}`")


@bot.on(Eiva_cmd(pattern=r"delsave\s+(.+)$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"delsave\s+(.+)$", allow_sudo=True))
async def delete_saved(event):
    await _delete_file(event, event.pattern_match.group(1), SAVED_DIR)


@bot.on(Eiva_cmd(pattern=r"delocal\s+(.+)$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"delocal\s+(.+)$", allow_sudo=True))
async def delete_download(event):
    await _delete_file(event, event.pattern_match.group(1), DOWNLOAD_DIR)


CmdHelp("managers").add_command(
    "ls", "[path]", "Lists repository files or files in a repository subdirectory."
).add_command(
    "ls_local", None, "Lists downloaded media."
).add_command(
    "ls_root", None, "Lists repository files."
).add_command(
    "ls_saved", None, "Lists saved files."
).add_command(
    "rnsaved", "from | to", "Renames a file in SAVED."
).add_command(
    "rnlocal", "from | to", "Renames a downloaded file."
).add_command(
    "delsave", "path", "Deletes a file from SAVED."
).add_command(
    "delocal", "path", "Deletes a file from the downloads folder."
).add_info("Bot file manager").add()
