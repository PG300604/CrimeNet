"""
Configure logging
"""
import logging
import atexit
from logging.handlers import QueueHandler, QueueListener
from sys import stdout, stderr
from queue import Queue
from .config import config


class SpecificLevelFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno == self.__level


logging.basicConfig(format=config["LOG_FORMAT"])
api_logger = logging.getLogger("api")
api_logger.setLevel(getattr(logging, config["LOG_LEVEL"]))

log_queue = Queue(-1)
queue_handler = QueueHandler(log_queue)
event_handler = logging.StreamHandler(stdout)
error_handler = logging.StreamHandler(stderr)
event_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)
event_handler.addFilter(SpecificLevelFilter(logging.INFO))
queue_listener = QueueListener(log_queue, event_handler, error_handler, respect_handler_level=True)
api_logger.addHandler(queue_handler)

queue_listener.start()

atexit.register(lambda: queue_listener.stop())
