import logging


class NullHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        pass


class NullLogger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.addHandler(NullHandler())
        self.setLevel(logging.NOTSET)
