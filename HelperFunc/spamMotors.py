# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import logging, requests
from config import Config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def SpamWatchAntiSpamCheck(userid):
    if not Config.SPAMWATCH_ANTISPAM_API: return None
    userid = str(userid)
    api = 'https://api.spamwat.ch'
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {Config.SPAMWATCH_ANTISPAM_API}"})
    req = session.request('get', f'{api}/banlist/{userid}')
    if not req.status_code == 200: return None
    info = "#Spamwatch Ban Info:"
    try:
        admin = req.json()['admin']
        id = req.json()['id']
        reason = req.json()['reason']
        message = req.json()['message']
        date = req.json()['date']
        if admin: info += f"\nAdmin: {admin}"
        if id: info += f"\nID: {id}"
        if reason: info += f"\nReason: {reason}"
        if message: info += f"\nMessage: {message}"
        if date: info += f"\nDate: {date}"
        LOGGER.info(info)
        return info
    except Exception as e:
        LOGGER.error(e)
        return None


def CombotAntiSpamCheck(userid):
    if not Config.COMBOT_CAS_ANTISPAM: return None
    userid = str(userid)
    api = f"https://api.cas.chat/check?user_id={userid}"
    session = requests.Session()
    req = session.request('get', api)
    if not int(req.status_code) == 200: return None
    if not bool(req.json()['ok']): return None
    info = "#Combot Ban Info:"
    result = req.json()['result']
    if not result: return info
    try:
        offenses = result['offenses']
        time_added = result['time_added']
        info += f"\nOffenses: {offenses}"
        info += f"\nTime: {time_added}"
        info += f"\nLink: <a href='https://cas.chat/query?u={userid}'>CAS Report</a>"
        info += f"\nCopy: <code>https://cas.chat/query?u={userid}</code>"
        LOGGER.info(info)
        return info
    except Exception as e:
        LOGGER.error(e)
        return None


def UsergeAntiSpamCheck(userid):
    if not Config.USERGE_ANTISPAM_API: return None
    userid = str(userid)
    api = f"https://api.userge.tk/ban?api_key={Config.USERGE_ANTISPAM_API}&user_id={userid}"
    session = requests.Session()
    req = session.request('get', api)
    if not bool(req.json()['success']): return None
    info = "#Userge Ban Info:"
    try:
        reason = req.json()['reason']
        date = req.json()['date']
        bb_user_id = req.json()['banned_by']['user_id']
        bb_user_name = req.json()['banned_by']['name']
        if reason: info += f"\nReason: {reason}"
        if date: info += f"\nDate: {date}"
        if bb_user_name: info += f"\nBanned by: {bb_user_name}"
        if bb_user_id: info += f" <a href='tg://user?id={bb_user_id}'>({str(bb_user_id)})</a>"
        LOGGER.info(info)
        return info
    except Exception as e:
        LOGGER.error(e)
        return None


def IntelliVoidSpamCheck(userid):
    if not Config.INTELLIVOID_ANTISPAM: return None
    userid = str(userid)
    api = f"https://api.intellivoid.net/spamprotection/v1/lookup?query={userid}"
    session = requests.Session()
    req = session.request('get', api)
    if not bool(req.json()['success']): return None
    info = "#IntelliVoid Ban Info:"
    try:
        is_potential_spammer = req.json()['results']['attributes']['is_potential_spammer']
        is_blacklisted = req.json()['results']['attributes']['is_blacklisted']
        language = req.json()['results']['language_prediction']['language']
        probability = req.json()['results']['language_prediction']['probability']
        spam_prediction = req.json()['results']['spam_prediction']['spam_prediction']
        ham_prediction = req.json()['results']['spam_prediction']['ham_prediction']
        last_updated = req.json()['results']['last_updated']
        info += f"\nPotential Spammer: {str(is_potential_spammer)}"
        info += f"\nBlacklisted: {str(is_blacklisted)}"
        if language: info += f"\nLanguage: {language}"
        if probability: info += f"\nProbability: {probability}"
        if spam_prediction: info += f"\nSpam Prediction: {spam_prediction}"
        if ham_prediction: info += f"\nHam Prediction: {ham_prediction}"
        if last_updated: info += f"\nLast Updated: {last_updated}"
        if language: info += f"\nLanguage: {language}"
        LOGGER.info(info)
        if bool(is_potential_spammer) or bool(is_blacklisted): return info
        else: return None
    except Exception as e:
        LOGGER.error(e)
        return None

