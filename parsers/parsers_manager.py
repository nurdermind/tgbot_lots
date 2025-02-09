import asyncio
import os
from concurrent.futures import ProcessPoolExecutor

from logger_config import logger
from parsers.catalog_lot_online_parser import get_current_price as get_current_price_catalog_lot_online
from parsers.roseltorg import get_current_price as get_current_price_roseltorg
from parsers.rts_tender_parser import get_current_price as get_current_price_rts_tender
from parsers.sberbank_parser import get_current_price as get_current_price_sberbank


def run_async_parser_sync(parser, url):
    logger.info(f"Процесс {os.getpid()} начал парсинг для {url}")
    result = asyncio.run(parser(url))
    logger.info(f"Процесс {os.getpid()} завершил парсинг для {url}")
    return result


class ParsersManager:
    def __init__(self):
        self.parsers = {
            'catalog.lot-online.ru': get_current_price_catalog_lot_online,
            'i.rts-tender.ru': get_current_price_rts_tender,
            'utp.sberbank-ast.ru': get_current_price_sberbank,
            '178fz.roseltorg.ru': get_current_price_roseltorg,
        }
        self.executor = ProcessPoolExecutor()

    def get_parser(self, url):
        for domain, parser in self.parsers.items():
            if domain in url:
                return parser
        raise ValueError(f"Нет доступного парсера для URL: {url}")

    async def get_price(self, url):
        parser = self.get_parser(url)
        loop = asyncio.get_running_loop()

        if asyncio.iscoroutinefunction(parser):
            price = await loop.run_in_executor(self.executor, run_async_parser_sync, parser, url)
        else:
            price = await loop.run_in_executor(self.executor, parser, url)

        logger.info(f"Цена успешно получена для сайта: {url}")
        return price

    def shutdown(self):
        self.executor.shutdown()
