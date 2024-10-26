import logging
import colorlog
from logging import FileHandler

LOG_FILE = "app.log"

log_colors = {
    'DEBUG': 'white',
    'INFO': 'white',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

file_handler = FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = colorlog.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    log_colors=log_colors
))

logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
