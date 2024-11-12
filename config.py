from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("No TELEGRAM_TOKEN set for Telegram bot")

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for the database connection")

SMS_API_KEY = os.getenv('SMS_API_KEY')
if not SMS_API_KEY:
    raise ValueError("No SMS_API_KEY set for Telegram bot")

APP_URL = os.getenv('APP_URL')
if not APP_URL:
    raise ValueError("No APP_URL set")

TO_PHONE = os.getenv('TO_PHONE')
if not TO_PHONE:
    raise ValueError("No TO_PHONE set")

TELEGRAM_IDS = os.getenv('TELEGRAM_IDS')
if not TELEGRAM_IDS:
    raise ValueError("No TELEGRAM_IDS set")

TLY_API = os.getenv('TLY_API')
if not TLY_API:
    raise ValueError("No TLY_API set")
