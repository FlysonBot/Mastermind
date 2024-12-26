from os import path

from appdirs import user_log_dir

from mastermind.libs.logs.logger import Logger


class ClientLogger(Logger):
    def __init__(self, logger_name: str):
        filepath = path.join(user_log_dir("mastermind-ai"), "client.log")
        super().__init__(filepath, logger_name)
