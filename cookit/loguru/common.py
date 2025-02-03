from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from typing import Union

from loguru import logger

from ..common import LazyGetterType, lazy_get


@contextmanager
def logged_suppress(
    msg: "LazyGetterType[str, [Exception]]",
    *t: type[Exception],
    level: Union[int, str] = "ERROR",
    log_stack: bool = True,
    debug_stack: bool = False,
    append_exc_msg: bool = False,
) -> Iterator[None]:
    try:
        yield
    except Exception as e:
        if t and (not isinstance(e, t)):
            raise

        msg_str = lazy_get(msg, e)
        if append_exc_msg:
            msg_str += f": {type(e).__name__}: {e}"

        lg = logger.opt(exception=e if log_stack else False, depth=2)
        lg.log(level, msg_str)

        if debug_stack:
            logger.opt(exception=e, depth=2).debug("Stacktrace")
        return


warning_suppress = partial(
    logged_suppress,
    level="WARNING",
    log_stack=False,
    debug_stack=True,
    append_exc_msg=True,
)
