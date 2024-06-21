from contextlib import contextmanager
from typing import Iterator, Type, Union

from loguru import logger

from ..common import LazyGetterType, lazy_get


@contextmanager
def logged_suppress(
    msg: "LazyGetterType[str, [Exception]]",
    *t: Type[Exception],
    level: Union[int, str] = "ERROR",
) -> Iterator[None]:
    try:
        yield
    except Exception as e:
        if t and (not isinstance(e, t)):
            raise
        logger.opt(exception=e).log(level, lazy_get(msg, e))
        return
