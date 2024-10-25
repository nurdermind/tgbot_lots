import logging
import colorlog
from logging import FileHandler

# Log file path
LOG_FILE = "app.log"

# Log color configuration
log_colors = {
    'DEBUG': 'white',
    'INFO': 'white',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

# Configure file handler (no colors, just plain text)
file_handler = FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Configure console handler with colors
console_handler = colorlog.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    log_colors=log_colors
))

# Configure the logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all log levels
logger.addHandler(file_handler)
logger.addHandler(console_handler)
