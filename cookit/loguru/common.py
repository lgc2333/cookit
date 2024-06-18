from contextlib import contextmanager
from typing import Type

from loguru import logger

from cookit.common import LazyGetterType, lazy_get


@contextmanager
def logged_suppress(msg: LazyGetterType[str, [Exception]], *t: Type[Exception]):
    try:
        yield
    except Exception as e:
        if t and (not isinstance(e, t)):
            raise
        logger.exception(lazy_get(msg, e))
        return
