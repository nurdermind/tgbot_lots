from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("No TELEGRAM_TOKEN set for Telegram bot")

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for the database connection")

CALLER_API_KEY = os.getenv('CALLER_API_KEY')
if not CALLER_API_KEY:
    raise ValueError("No CALLER_API_KEY set for Telegram bot")

CAMPAIGN_ID = os.getenv('CAMPAIGN_ID')
if not CAMPAIGN_ID:
    raise ValueError("No CAMPAIGN_ID set")

APP_URL = os.getenv('APP_URL')
if not APP_URL:
    raise ValueError("No APP_URL set")
