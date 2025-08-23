import logging
from logging.handlers import RotatingFileHandler
import json

# Create a custom logger
logger = logging.getLogger("support_bot")
logger.setLevel(logging.INFO)  # Log INFO and above

# Create a file handler that rotates logs after 5 MB, keep 3 backups
file_handler = RotatingFileHandler("support_bot.log", maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.INFO)

# Create a console handler (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_info(obj, msg=""):
    if isinstance(obj, (dict, list)):
        log_msg = f"{msg} | Data: {json.dumps(obj, indent=2)}"
    else:
        log_msg = f"{msg} | {str(obj)}"
    logger.info(log_msg)
