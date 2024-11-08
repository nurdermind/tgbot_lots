import httpx
from urllib.parse import quote
from logger_config import logger
from config import TO_PHONE, SMS_API_KEY

async def send_sms(message):
    sender = 'INFORM'
    url = f"http://smspilot.ru/api.php?send={quote(message)}&to={TO_PHONE}&from={sender}&apikey={SMS_API_KEY}&format=json"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            j = response.json()

            if 'error' in j:
                print(f"Ошибка: {j['error']['description_ru']}")
            else:
                print(f"ID: {j['send'][0]['server_id']}")
    except httpx.RequestError as e:
        logger.error(f"Ошибка сети при отправке SMS: {e}")
    except Exception as e:
        logger.exception(f"Не удалось отправить SMS: {e}")

