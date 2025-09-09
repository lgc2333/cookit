from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from functools import partial
from types import TracebackType
from typing import TYPE_CHECKING, Any

from loguru import logger

from ..common import LazyGetterType, lazy_get

# 别问我为什么不直接写成类，因为 loguru 拿不到 frame 我又不会解决

if TYPE_CHECKING:

    class logged_suppress(AbstractContextManager[Any, bool]):  # noqa: N801
        def __init__(
            self,
            msg: "LazyGetterType[str, [Exception]]",
            *t: type[Exception],
            level: int | str = "ERROR",
            log_stack: bool = True,
            debug_stack: bool = False,
            append_exc_msg: bool = False,
        ): ...
        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
        ) -> bool: ...


else:

    @contextmanager
    def logged_suppress(
        msg: "LazyGetterType[str, [Exception]]",
        *t: type[Exception],
        level: int | str = "ERROR",
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


def log_exception_warning(
    e: BaseException,
    msg: str,
    debug_stacktrace: bool = True,
):
    logger.opt(depth=1).warning(f"{msg}: {type(e).__name__}: {e}")
    if debug_stacktrace:
        logger.opt(depth=1, exception=e).debug("Stacktrace")
