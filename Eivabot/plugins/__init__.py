import datetime
from Eivabot import *
from Eivabot.config import Config
from Eivabot.helpers import *
from Eivabot.utils import *
from Eivabot.random_strings import *
from Eivabot.version import __Eiva__
from telethon import version


Eiva_USER = bot.me.first_name
ForGo10God = bot.uid
Eiva_mention = f"[{Eiva_USER}](tg://user?id={ForGo10God})"
Eiva_logo = "./Eivabot/resources/pics/Eivabot_logo.jpg"
cjb = "./Eivabot/resources/pics/cjb.jpg"
restlo = "./Eivabot/resources/pics/rest.jpeg"
shuru = "./Eivabot/resources/pics/shuru.jpg"
hl = Config.HANDLER
shl = Config.SUDO_HANDLER
Eiva_ver = __Eiva__
tel_ver = version.__version__

async def get_user_id(ids):
    return int(ids) if str(ids).isdigit() else (await bot.get_entity(ids)).id

sudos = Config.SUDO_USERS
is_sudo = "True" if sudos else "False"
abus = Config.ABUSE
abuse_m = "Enabled" if abus == "ON" else "Disabled"
START_TIME = datetime.datetime.now()
uptime = f"{str(datetime.datetime.now() - START_TIME).split('.')[0]}"
my_channel = Config.MY_CHANNEL or "Its_EivaBot"
my_group = Config.MY_GROUP or "EivaBot_Chat"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/TheEiva"
Eiva_channel = f"[†hê EIVABOT]({chnl_link})"
grp_link = "https://t.me/EivaSupport"
Eiva_grp = f"[EIVABOT Group]({grp_link})"

WELCOME_FORMAT = """**Use these fomats in your welcome note to make them attractive.**
  {mention} :  To mention the user
  {title} : To get chat name in message
  {count} : To get group members
  {first} : To use user first name
  {last} : To use user last name
  {fullname} : To use user full name
  {userid} : To use userid
  {username} : To use user username
  {my_first} : To use my first name
  {my_fullname} : To use my full name
  {my_last} : To use my last name
  {my_mention} : To mention myself
  {my_username} : To use my username
"""
# will add more soon

# Eivabot
