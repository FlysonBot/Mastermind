import sys
from os import path

from appdirs import user_log_dir

from mastermind.libs.logs.logger import Logger


class ServerLogger(Logger):
    def __init__(self, logger_name: str):
        filepath = path.join(user_log_dir("mastermind-ai"), "server.log")
        super().__init__(filepath, logger_name)


class ServerExceptionLogger(ServerLogger):
    def __init__(self):
        super().__init__("ExceptionLogger")

    def setup_exception_hook(self):
        sys.excepthook = self.handle_exception

    def handle_exception(
        self, exc_type: type, exc_value: BaseException, exc_traceback: str
    ):
        self.error(f"Exception: {exc_type.__name__}: {exc_value}")
        self.error(f"Traceback: {exc_traceback}")
