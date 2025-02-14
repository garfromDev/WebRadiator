from .CST import CST
import logging
from flask.logging import default_handler

logger = logging.getLogger('main')  # grabs underlying WSGI logger
handler = logging.FileHandler(CST.LOG_FILE)  # creates handler for the log file
logger.addHandler(handler)
logger.addHandler(default_handler)