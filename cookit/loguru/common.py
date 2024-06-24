from contextlib import contextmanager
from functools import partial
from typing import Iterator, Type, Union

from loguru import logger

from ..common import LazyGetterType, lazy_get


@contextmanager
def logged_suppress(
    msg: "LazyGetterType[str, [Exception]]",
    *t: Type[Exception],
    level: Union[int, str] = "ERROR",
    log_stack: bool = True,
    debug_stack: bool = False,
) -> Iterator[None]:
    try:
        yield
    except Exception as e:
        if t and (not isinstance(e, t)):
            raise
        lg = logger.opt(exception=e) if log_stack else logger
        lg.log(level, lazy_get(msg, e))
        if debug_stack:
            logger.opt(exception=e).debug("Stacktrace")
        return


warning_suppress = partial(
    logged_suppress,
    level="WARNING",
    log_stack=False,
    debug_stack=True,
)
