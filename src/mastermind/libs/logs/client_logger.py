import atexit
import sys
import traceback
from os import path

from appdirs import user_log_dir

from mastermind.libs.logs.logger import Logger


class ClientLogger(Logger):
    """Logger for client-side operations."""

    started: bool = False
    filepath: str = path.join(user_log_dir("mastermind-ai"), "client.log")

    def __init__(self, logger_name: str) -> None:
        super().__init__(self.filepath, logger_name)

        if not self.started:
            Logger(self.filepath, "Client Status").info("Client logging started")
            atexit.register(lambda: ClientLogger.close())
            self.started = True

    @classmethod
    def close(cls) -> None:
        Logger(cls.filepath, "Client Status").info("Client logging stopped")


class ClientExceptionLogger(ClientLogger):
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
