# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from HelperFunc.authUserCheck import AuthUserCheck
from HelperFunc.message import sendMessage
from HelperFunc.spamMotors import CombotAntiSpamCheck, IntelliVoidSpamCheck, SpamWatchAntiSpamCheck, UsergeAntiSpamCheck
from config import Config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command(Config.CHECK_COMMAND))
async def check(client, message: Message):
    userid = message.from_user.id
    if not Config.CHECK_ALLOWED:
        return LOGGER.info("Checking Disabled. Read Readme.")
    elif Config.CHECK_ALLOWED == 'auths':
        if not await AuthUserCheck(message): return LOGGER.info("Checking only for Auth Users.")
    elif Config.CHECK_ALLOWED == 'owner':
        if userid != Config.OWNER_ID: return LOGGER.info("Checking only for Owner.")
    url = None
    helpstr = f"Send like: /{Config.CHECK_COMMAND[0]} 515151521"
    helpstr += f"\nFor check yourself, send: /{Config.CHECK_COMMAND[0]} {str(userid)}"
    if not message.reply_to_message:
        url = message.text.split(' ', 1)
        try: url = url[1]
        except: return await sendMessage(message, helpstr)
    else: url = message.reply_to_message.text
    try: userid = int(url)
    except:
        helpstr += "\nOnly send user id. Integer. Like 515187151"
        return await sendMessage(message, helpstr)
    tumad = message.from_user.mention()
    SpamWatch = None
    Combot = None
    Userge = None
    IntelliVoid = None
    if Config.SPAMWATCH_ANTISPAM_API: SpamWatch = SpamWatchAntiSpamCheck(userid)
    if Config.COMBOT_CAS_ANTISPAM: Combot = CombotAntiSpamCheck(userid)
    if Config.USERGE_ANTISPAM_API: Userge = UsergeAntiSpamCheck(userid)
    if Config.INTELLIVOID_ANTISPAM: IntelliVoid = IntelliVoidSpamCheck(userid)
    strop = f"{tumad} ({str(userid)}) Check Results:"
    if SpamWatch: strop += f"\n\n{SpamWatch}"
    if Combot: strop += f"\n\n{Combot}"
    if Userge: strop += f"\n\n{Userge}"
    if IntelliVoid: strop += f"\n\n{IntelliVoid}"
    if not (SpamWatch or Combot or Userge or IntelliVoid):
        strop += "\nClean User. Checked With:"
        if Config.SPAMWATCH_ANTISPAM_API: strop += "\nSpamWatch"
        if Config.COMBOT_CAS_ANTISPAM: strop += "\nCombot"
        if Config.USERGE_ANTISPAM_API: strop += "\nUserge"
        if Config.INTELLIVOID_ANTISPAM: strop += "\nIntelliVoid"
    reply_markup = None
    if Config.UPDATES_CHANNEL:
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                text = "🔥 Güncellemeler / Updates",
                url = "https://t.me/" + Config.UPDATES_CHANNEL)
                ]
            ])
    await sendMessage(message,strop,reply_markup)
