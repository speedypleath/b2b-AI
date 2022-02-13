import logging
from logging.handlers import TimedRotatingFileHandler
import sys

FORMATTER = logging.Formatter('["%(levelname)s" - %(asctime)s]: %(message)s in %(pathname)s:%(lineno)d', "%Y-%m-%d %H:%M:%S")
LOGGER_NAME = 'b2b-AI'

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_file_handler(log_file: str):
   file_handler = TimedRotatingFileHandler(log_file, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_logger(log_file: str, level: int = logging.DEBUG, handle_console = False):
   logger = logging.getLogger(LOGGER_NAME)
   logger.setLevel(level)
   if handle_console:
      logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler(log_file))
   return logger