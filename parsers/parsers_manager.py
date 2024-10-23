from select import select

from parsers.catalog_lot_online_parser import get_current_price as get_current_price_catalog_lot_online

class ParsersManager:
    def __init__(self):
        self.parsers = {
            'catalog.lot-online.ru': get_current_price_catalog_lot_online,
        }

    def get_parser(self, url):
        for domain, parser in self.parsers.items():
            if domain in url:
                return self.parsers.get(domain)
                return parser
        raise ValueError(f"No parser available for URL: {url}")

    async def get_price(self, url):
        parser = self.get_parser(url)
        return await parser(url)
