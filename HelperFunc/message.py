# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import time, logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


async def sendMessage(toReplyMessage, replyText, replyButtons = None):
    try:
        return await toReplyMessage.reply_text(replyText,
            disable_web_page_preview=True,
            parse_mode='html',
            quote=True,
            reply_markup = replyButtons)
    except FloodWait as e:
        time.sleep(e.x)
        LOGGER.info(str(e))
        return await sendMessage(toReplyMessage, replyText, replyButtons)
    except Exception as e:
        LOGGER.info(str(e))

async def sendDocument(toReplyDocument: Message, filePath: str):
    try:
        return await toReplyDocument.reply_document(filePath)
    except FloodWait as e:
        await time.sleep(e.x)
        LOGGER.info(str(e))
        return await sendDocument(toReplyDocument, filePath)
    except Exception as e:
        LOGGER.info(str(e))
