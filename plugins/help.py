# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram.types.messages_and_media.message import Message
from HelperFunc.authUserCheck import AuthUserCheck


from HelperFunc.message import sendMessage
from config import Config
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command(Config.HELP_COMMANDS))
async def help(client, message: Message):
	if not await AuthUserCheck(message): return
	tumad = message.from_user.mention()
	sampleText = f"<a href='https://github.com/HuzunluArtemis/AntiSpamBot'>🍁</a> Esenlikler / Hi {tumad}\n\n"
	sampleText += "I can fight with spam with power of:"
	sampleText += "\n- SpamWatch AntiSpam"
	sampleText += "\n- Combot AntiSpam (CAS)"
	sampleText += "\n- Userge AntiSpam"
	sampleText += "\n- IntelliVoid AntiSpam (AI)"
	sampleText += "\n- Or Ban All Newcomers"
	sampleText += "\n\nMake your group SuperGroup\nGive ban permission to me."
	sampleText += "\nDont forget filling variables."
	sampleText += "\n\nActive Protections For This Bot:"
	sampleText += f"\n- SpamWatch: {str(bool(Config.SPAMWATCH_ANTISPAM_API))}"
	sampleText += f"\n- Combot: {str(bool(Config.COMBOT_CAS_ANTISPAM))}"
	sampleText += f"\n- Userge: {str(bool(Config.USERGE_ANTISPAM_API))}"
	sampleText += f"\n- IntelliVoid: {str(bool(Config.INTELLIVOID_ANTISPAM))}"
	sampleText += f"\n- Newcomers: {str(bool(Config.BAN_ALL_NEWCOMERS))}"
	reply_markup = None
	if Config.UPDATES_CHANNEL:
		reply_markup=InlineKeyboardMarkup(
			[
				[InlineKeyboardButton(
				text = "🔥 Güncellemeler / Updates",
				url = "https://t.me/" + Config.UPDATES_CHANNEL)
				]
			])
	await sendMessage(message,sampleText,reply_markup)
