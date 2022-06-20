# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import logging
from config import Config
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
import logging, os, time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def ReadableTime(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result



class Bot(Client):

    def __init__(self):
        super().__init__(
            session_name='antispambot',
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=343,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        LOGGER.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        if Config.OWNER_ID != 0:
            try:
                await self.send_message(
                    text= "🇬🇧 i reborn from the ashes of darkness\n🇦🇿 qaranlığın küllərindən yenidən yarandım",
                    chat_id=Config.OWNER_ID)
            except Exception as t:
                LOGGER.error(str(t))

    async def stop(self, *args):
        if Config.OWNER_ID != 0:
            texto = f"🇬🇧 I took my last breath.\nthe age i died: {ReadableTime(time.time() - Config.botStartTime)}" + \
                    f"\n\n🇦🇿 son nəfəsimi verdim.\nöləndə yaşım: {ReadableTime(time.time() - Config.botStartTime)}"
            try:
                await self.send_message(text= texto,chat_id=Config.OWNER_ID)
            except Exception as t:
                LOGGER.warning(str(t))
        await super().stop()
        LOGGER.info(msg="App Stopped.")
        exit()

app = Bot()
app.run()
