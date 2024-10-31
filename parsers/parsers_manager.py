from parsers.catalog_lot_online_parser import get_current_price as get_current_price_catalog_lot_online
from parsers.rts_tender_parser import get_current_price as get_current_price_rts_tender
from parsers.sberbank_parser import get_current_price as get_current_price_sberbank

class ParsersManager:
    def __init__(self):
        self.parsers = {
            'catalog.lot-online.ru': get_current_price_catalog_lot_online,
            'i.rts-tender.ru': get_current_price_rts_tender,
            'utp.sberbank-ast.ru': get_current_price_sberbank,
        }

    def get_parser(self, url):
        for domain, parser in self.parsers.items():
            if domain in url:
                return parser
        raise ValueError(f"No parser available for URL: {url}")

    async def get_price(self, url):
        parser = self.get_parser(url)

        return await parser(url)
