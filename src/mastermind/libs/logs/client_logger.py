import atexit
import sys
import traceback
from os import path

from appdirs import user_log_dir

from mastermind.libs.logs.logger import Logger


class ClientLogger(Logger):
    """Logger for client-side operations."""

    started = False
    filepath = path.join(user_log_dir("mastermind-ai"), "client.log")

    def __init__(self, logger_name: str):
        super().__init__(self.filepath, logger_name)

        if not self.started:
            Logger(self.filepath, "Client Status").info("Client logging started")
            atexit.register(lambda: ClientLogger.close())
            self.started = True

    @classmethod
    def close(cls):
        Logger(cls.filepath, "Client Status").info("Client logging stopped")


class ClientExceptionLogger(ClientLogger):
    def __init__(self):
        super().__init__("ExceptionLogger")

    def setup_exception_hook(self):
        sys.excepthook = self.handle_exception

    def handle_exception(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: traceback.TracebackException,
    ):
        traceback_message = "\n".join(  # type: ignore
            traceback.format_exception(exc_type, exc_value, exc_traceback)  # type: ignore
        )
        self.error(f"Exception: {exc_type.__name__}: {exc_value}")
        self.error(f"Traceback:\n{traceback_message}")
