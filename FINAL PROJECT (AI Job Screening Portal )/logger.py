import logging
import os
from config import LOG_FILE

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("screening_portal")
logger.setLevel(logging.DEBUG)

terminal_handler = logging.StreamHandler()
terminal_handler.setLevel(logging.INFO)
terminal_handler.setFormatter(logging.Formatter("%(levelname)s  %(message)s"))

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s  %(levelname)s  %(message)s"))

logger.addHandler(terminal_handler)
logger.addHandler(file_handler)