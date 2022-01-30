# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
import logging, requests
from HelperFunc.authUserCheck import AuthUserCheck
from HelperFunc.message import sendMessage
from HelperFunc.spamMotors import CombotAntiSpamCheck, IntelliVoidSpamCheck, SpamWatchAntiSpamCheck, UsergeAntiSpamCheck
from config import Config
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.group & filters.new_chat_members)
async def antiSpam(client: Client, message: Message):
    if not await AuthUserCheck(message): return
    new_members = message.new_chat_members
    chatid = message.chat.id
    mfu = message.from_user
    if not chatid: return LOGGER.warning("not chatid")
    if not mfu: return LOGGER.warning("not mfu")
    botID = await client.get_me()
    if botID in new_members:
        helpstr = "You Added Me.\nMake your group SuperGroup\nGive ban permission to me." \
            f"\nMaybe you want read /{Config.HELP_COMMANDS[0]}"
        return await sendMessage(message, helpstr)
    a = await client.get_chat_member(chatid, botID.id)
    if not a.can_restrict_members:
        return await sendMessage(message, "🇬🇧 Give ban permission.")
    for p in new_members:
        banned = None
        mesg = None
        if Config.BAN_ALL_NEWCOMERS:
            banned = f"#Newcomer Ban"
        if not banned:
            if Config.SPAMWATCH_ANTISPAM_API: banned = SpamWatchAntiSpamCheck(p.id)
        if not banned:
            if Config.COMBOT_CAS_ANTISPAM: banned = CombotAntiSpamCheck(p.id)
        if not banned:
            if Config.USERGE_ANTISPAM_API: banned = UsergeAntiSpamCheck(p.id)
        if not banned:
            if Config.INTELLIVOID_ANTISPAM: banned = IntelliVoidSpamCheck(p.id)
        if not banned:
            uclean = f"Welcome clean user {p.mention()} ({str(p.id)})"
            if not Config.USER_CLEAN_MESSAGE: return LOGGER.info(uclean)
            else: mesg = await sendMessage(message, uclean)
        else:
            success = None
            try:
                if not Config.DONT_BAN:
                    await client.ban_chat_member(chatid, p.id)
                    success = "Success"
                else:
                    success = "Banning Disabled"
            except Exception as o:
                success = "Unsuccess"
                LOGGER.error(o)
            swtc = f"{mfu.mention()} Added: {p.mention()}"
            swtc += f"\nID: <code>{str(p.id)}</code>"
            swtc += f"\nBan: {success}"
            swtc += f"\n{banned}"
            if Config.SILENT_BAN: return LOGGER.info(swtc)
            else: mesg = await sendMessage(message, swtc)
        if not mesg: return
        if not Config.AUTO_DEL_SEC: return
        time.sleep(Config.AUTO_DEL_SEC)
        try: await mesg.delete()
        except Exception as e: LOGGER.error(e)

