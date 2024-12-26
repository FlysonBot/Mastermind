import logging
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, log_file_path: str, logger_name: str):
        self.log_file_path = log_file_path
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.create_file_handler()

    def create_file_handler(self):
        file_handler = RotatingFileHandler(
            self.log_file_path, maxBytes=1024 * 1024 * 10, backupCount=10
        )
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s (File: %(filename)s, Line: %(lineno)d)",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

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
