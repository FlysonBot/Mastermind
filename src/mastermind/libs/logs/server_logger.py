import atexit
import sys
import traceback
from os import path

from appdirs import user_log_dir

from .logger import Logger


class ServerLogger(Logger):
    """Logger for server-side operations."""

    started: bool = False
    filepath: str = path.join(user_log_dir("mastermind-ai"), "server.log")

    def __init__(self, logger_name: str) -> None:
        super().__init__(self.filepath, logger_name)

        if not self.started:
            Logger(self.filepath, "Server Status").info("Server logging started")
            atexit.register(lambda: ServerLogger.close())
            self.started = True

    @classmethod
    def close(cls) -> None:
        Logger(cls.filepath, "Server Status").info("Server logging stopped")


class ServerExceptionLogger(ServerLogger):
    def __init__(self) -> None:
        super().__init__("ExceptionLogger")

    def setup_exception_hook(self) -> None:
        sys.excepthook = self.handle_exception  # type: ignore

    def handle_exception(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: traceback.TracebackException,
    ) -> None:
        traceback_message: str = "\n".join(  # type: ignore
            traceback.format_exception(exc_type, exc_value, exc_traceback)  # type: ignore
        )
        self.error(f"Exception: {exc_type.__name__}: {exc_value}")
        self.error(f"Traceback:\n{traceback_message}")
