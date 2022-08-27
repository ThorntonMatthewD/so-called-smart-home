"""Handles logging within the application"""

import logging
import time
from datetime import datetime

logging.basicConfig(
    filename="../log/environment-sensor-monitor.log", encoding="utf-8", level=logging.INFO
)


def get_timestamp():
    """Gets current time and create formatted timestamp for logs"""
    return datetime.fromtimestamp(time.time())


def log_error(exception, context):
    """Logs errors to the error file"""
    logging.error("[%s] ERROR - %s; Context - %s", get_timestamp(), exception, context)
