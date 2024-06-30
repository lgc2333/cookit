from typing import TYPE_CHECKING, Callable, List, Optional, Type, Union

from loguru import logger

if TYPE_CHECKING:
    from loguru import Message, Record

    class NotRequiredRecord(Record, total=False):
        pass


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

    def should_log(
        self,
        *,
        exception: Union[BaseException, Type[BaseException], None] = ...,
        level_str: Optional[str] = None,
        level_no: Optional[int] = None,
        message: Optional[str] = None,
        message_fullmatch: bool = True,
    ):
        def checker(m: "Message"):
            record = m.record
            if exception is not ...:
                r_exception = record.get("exception")
                if exception is None:
                    assert r_exception is None
                else:
                    assert r_exception
                    assert (
                        r_exception.type is exception
                        if isinstance(exception, type)
                        else r_exception.value is exception
                    )
            if level_str is not None:
                assert record["level"].name == level_str
            if level_no is not None:
                assert record["level"].no == level_no
            if message is not None:
                r_message = record["message"]
                assert (
                    message == r_message if message_fullmatch else message in r_message
                )

        self.checker_stack.append(checker)

    def check(self):
        for checker in self.checker_stack:
            checker(self.log_stack.pop(0))
