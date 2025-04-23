"""
Logger configuration for the NetworkSecurity package.

This module sets up a timestamped log file inside a 'logs' directory.
Logs will include timestamp, line number, logger name, log level, and message.
"""

from datetime import datetime
import logging
import os

# Define the directory where logs will be saved
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Generate a log filename with the current timestamp
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.log"
log_file_path = os.path.join(LOG_DIR, LOG_FILE)

# Configure the logging module
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s:%(levelname)s: %(message)s",
)
