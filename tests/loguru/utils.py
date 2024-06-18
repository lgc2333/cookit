from typing import TYPE_CHECKING, Callable, List, Optional

import pytest
from loguru import logger

if TYPE_CHECKING:
    from loguru import Message

LoguruHandler = Callable[["Message"], None]


def make_handler(log_stack: List["Message"]) -> LoguruHandler:
    def handler(message: "Message") -> None:
        log_stack.append(message)

    return handler


class LoggingContext:
    def __init__(self) -> None:
        self.log_stack: List["Message"] = []
        self.checker_stack: List[Callable[["Message"], None]] = []
        self.id: Optional[int] = None

    def __enter__(self):
        self.id = logger.add(make_handler(self.log_stack))
        return self

    def __exit__(self, *_):
        if self.id is not None:
            logger.remove(self.id)
        self.check()

    def should_message(self, msg: str):
        def checker(message: "Message"):
            if msg == (actual := message.record["message"]):
                return
            pytest.fail(f'Logging message mismatch, expected "{msg}", got "{actual}"')

        self.checker_stack.append(checker)

    def should_contain_message(self, msg: str):
        def checker(message: "Message"):
            if msg in (actual := message.record["message"]):
                return
            pytest.fail(f'Logging message does not contain "{msg}", got "{actual}"')

        self.checker_stack.append(checker)

    def check(self):
        for checker in self.checker_stack:
            checker(self.log_stack.pop(0))


def test_logger():
    return LoggingContext()
