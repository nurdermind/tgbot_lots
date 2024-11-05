import httpx
from logger_config import logger
from config import CALLER_API_KEY, TO_PHONE, FROM_PHONE

async def make_call():
    url = "https://lk.zvonobot.ru/apiCalls/create"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "apiKey": CALLER_API_KEY,
        "phone": TO_PHONE,
        "outgoingPhone": FROM_PHONE,
        "record": {
            "text": (
                "Цена лота изменилась. Подробная информация отправлена в телеграмм бот. "
                "Можете выключить звонок, так как текст дальше предназначен для того чтобы "
                "сделать аудиосообщение большим"
            ),
            "gender": 1
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)

        if response.status_code == 200:
            logger.info("Вызов успешно создан.")
        else:
            logger.error(f"Ошибка при создании вызова: {response.status_code} - {response.text}")
    except Exception as e:
        logger.exception(f"Не удалось выполнить вызов: {e}")
