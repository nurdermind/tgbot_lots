import asyncio
from utils.database import get_all_lots, update_lot_price
from utils.notifier import send_telegram_message
from parsers.parsers_manager import ParsersManager

async def track_single_lot(lot, manager):
    while True:
        try:
            current_price = await manager.get_price(lot.url)

            if current_price != lot.current_price:
                message = f"Цена изменилась для {lot.name}! Новая цена: {current_price}"
                send_telegram_message(lot.owner_id, message)

                update_lot_price(lot, current_price)

        except Exception as e:
            print(f"Ошибка при обработке лота {lot.url}: {e}")

        await asyncio.sleep(5)

async def track_lots():
    manager = ParsersManager()
    lots = get_all_lots()

    tasks = [track_single_lot(lot, manager) for lot in lots]

    await asyncio.gather(*tasks)

# Main entry point
def run_tracking():
    asyncio.run(track_lots())