import cv2
import os
import io
import random
import shutil
import re
import textwrap
import lottie

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

from . import *


path = "./Eivamify/"
if not os.path.isdir(path):
    os.makedirs(path)


@bot.on(Eiva_cmd(pattern="mmf ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mmf ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eod(event, "You need to reply to an image with .mmf` 'text on top' ; 'text on bottom'")
        return
    await eor(event, "🤪 **Memifying...**")
    reply = await event.get_reply_message()
    imgs = await bot.download_media(reply.media, path)
    img = cv2.VideoCapture(imgs) 
    tal, semx = img.read()
    cv2.imwrite("kraken.webp", semx)
    text = event.pattern_match.group(1)
    webp_file = await draw_meme_text("kraken.webp", text)
    await event.client.send_file(
        event.chat_id, webp_file, reply_to=event.reply_to_msg_id
    )
    await event.delete()
    shutil.rmtree(path)
    os.remove("kraken.webp")
    os.remove(webp_file)


@bot.on(Eiva_cmd(pattern="mms ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mms ?(.*)", allow_sudo=True))
async def sed(Eivaboy):
    if Eivaboy.fwd_from:
        return
    if not Eivaboy.reply_to_msg_id:
        await eod(Eivaboy, "You need to reply to an image with .mms` 'text on top' ; 'text on bottom'")
        return
    await eor(Eivaboy, "🤪 **Memifying...**")
    reply = await Eivaboy.get_reply_message()
    imgs = await bot.download_media(reply.media, path)
    img = cv2.VideoCapture(imgs) 
    tal, semx = img.read()
    cv2.imwrite("kraken.webp", semx)
    text = Eivaboy.pattern_match.group(1)
    photo = await draw_meme("kraken.webp", text)
    await Eivaboy.client.send_file(
        Eivaboy.chat_id, photo, reply_to=Eivaboy.reply_to_msg_id
    )
    await Eivaboy.delete()
    shutil.rmtree(path)
    os.remove("kraken.webp")
    os.remove(photo)
    
@bot.on(Eiva_cmd(pattern="doge(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="doge(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    Eiva = kraken.pattern_match.group(1)
    if not Eiva:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        elif Config.ABUSE == "ON":
            return await eor(kraken, "Abe chumtiye kuch likhne ke liye de")
        else:
            return await eor(kraken, "Doge need some text to make sticker.")

    troll = await bot.inline_query("DogeStickerBot", f"{(deEmojify(Eiva))}")
    if troll:
        await kraken.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await bot.send_file(
                kraken.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
     await eod(kraken, "Error 404:  Not Found")
     
    
CmdHelp("memify").add_command(
  "mmf", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in sticker format.", "mmf <reply to a img/stcr/gif> hii ; Eivao"
).add_command(
  "mms", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in image format.", "mms <reply to a img/stcr/gif> hii ; Eivao"
).add_command(
  "doge", "<text>", "Makes A Sticker of Doge with given text."
).add_info(
  "Make Memes on telegram 😉"
).add_warning(
  "✅ Harmless Module."
).add()
