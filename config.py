# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import logging, os, time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class Config(object):
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
    if not BOT_USERNAME.startswith('@'): BOT_USERNAME = '@' + BOT_USERNAME # bu satıra dokunmayın.
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", '')
    if len(UPDATES_CHANNEL) < 2: UPDATES_CHANNEL = None
    OWNER_ID = int(os.environ.get('OWNER_ID', 0)) # give your owner id # if given 0 shell will not works
    AUTH_IDS = [int(x) for x in os.environ.get("AUTH_IDS", "0").split()] # if open to everyone give 0
    AUTH_IDS.append(OWNER_ID)
    LOG_COMMAND = os.environ.get('LOG_COMMAND','log')
    LOG_COMMAND = [LOG_COMMAND, LOG_COMMAND+BOT_USERNAME] # bu satıra dokunmayın.

    # spam protections +
    
    BAN_ALL_NEWCOMERS =  os.environ.get('BAN_ALL_NEWCOMERS','False').lower() == 'true'

    COMBOT_CAS_ANTISPAM =  os.environ.get('COMBOT_CAS_ANTISPAM','False').lower() == 'true'

    INTELLIVOID_ANTISPAM = os.environ.get('INTELLIVOID_ANTISPAM','False').lower() == 'true'

    SPAMWATCH_ANTISPAM_API = os.environ.get('SPAMWATCH_ANTISPAM_API','')
    if len(SPAMWATCH_ANTISPAM_API) < 2: SPAMWATCH_ANTISPAM_API = None

    USERGE_ANTISPAM_API = os.environ.get('USERGE_ANTISPAM_API','')
    if len(USERGE_ANTISPAM_API) < 2: USERGE_ANTISPAM_API = None

    SILENT_BAN =  os.environ.get('SILENT_BAN','False').lower() == 'true'
    USER_CLEAN_MESSAGE =  os.environ.get('USER_CLEAN_MESSAGE','False').lower() == 'true'
    try: AUTO_DEL_SEC =  int(os.environ.get('AUTO_DEL_SEC','0'))
    except: AUTO_DEL_SEC = 0
    if AUTO_DEL_SEC == 0: AUTO_DEL_SEC = None

    # spam protections -

    if not (SPAMWATCH_ANTISPAM_API or COMBOT_CAS_ANTISPAM or USERGE_ANTISPAM_API or INTELLIVOID_ANTISPAM):
        LOGGER.error("no spam protection. enable one or more.")
        exit(1)

    botStartTime = time.time() # dont touch
    HELP_COMMANDS = ["start", "help", "about", "yardım", "h", "y",
        f"start{BOT_USERNAME}", f"help{BOT_USERNAME}", f"about{BOT_USERNAME}",
        f"yardım{BOT_USERNAME}", f"h{BOT_USERNAME}", f"y{BOT_USERNAME}"]
