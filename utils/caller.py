import requests
from logger_config import logger
from config import CALLER_API_KEY, CAMPAIGN_ID

CALLTOOLS_BASE_URL = 'https://zvonok.com'
CALLTOOLS_TIMEOUT = 30

async def make_call(phonenumber, text, speaker='Tatyana'):
    try:
        resp = requests.get(
            f'{CALLTOOLS_BASE_URL}/manager/cabapi_external/api/v1/phones/call/',
            params={
                'public_key': CALLER_API_KEY,
                'phone': phonenumber,
                'campaign_id': CAMPAIGN_ID,
                'text': text,
                'speaker': speaker,
            },
            timeout=CALLTOOLS_TIMEOUT
        )
        
        resp.raise_for_status()
        ret = resp.json()
        
        if 'status' in ret and ret['status'] == 'error':
            logger.error(f"Ошибка при отправке звонка: {ret['data']}")
            raise Exception(ret['data'])
        
        if 'call_id' in ret:
            logger.info(f"Звонок успешно отправлен на номер {phonenumber}, Call ID: {ret['call_id']}")
        else:
            logger.warning("Неожиданный ответ от сервера без call_id.")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при отправке звонка: {e}")
