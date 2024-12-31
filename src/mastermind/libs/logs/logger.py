import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:
    def __init__(self, log_file_path: str, logger_name: str):
        self.log_file_path = log_file_path
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(get_file_handler(log_file_path))

    def info(self, msg: str):
        self.logger.info(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)


def get_file_handler(log_file_path: str) -> RotatingFileHandler:
    ensure_log_file_exists(log_file_path)

    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=1024 * 1024 * 10, backupCount=10
    )
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    return file_handler


def ensure_log_file_exists(log_file_path: str):
    log_file = Path(log_file_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if not log_file.exists():
        log_file.touch()
