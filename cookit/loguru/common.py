from contextlib import AbstractContextManager
from functools import partial
from types import TracebackType
from typing import Optional, Union

from loguru import logger

from ..common import LazyGetterType, lazy_get


class logged_suppress(AbstractContextManager[None, bool]):  # noqa: N801
    def __init__(
        self,
        msg: "LazyGetterType[str, [BaseException]]",
        *t: type[Exception],
        level: Union[int, str] = "ERROR",
        log_stack: bool = True,
        debug_stack: bool = False,
        append_exc_msg: bool = False,
    ) -> None:
        self.msg = msg
        self.t = t
        self.level = level
        self.log_stack = log_stack
        self.debug_stack = debug_stack
        self.append_exc_msg = append_exc_msg

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_inst: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        if (not (exc_type and exc_inst)) or (
            self.t and (not isinstance(exc_inst, self.t))
        ):
            return False

        msg_str = lazy_get(self.msg, exc_inst)
        if self.append_exc_msg:
            msg_str += f": {exc_type.__name__}: {exc_inst}"

        lg = logger.opt(exception=exc_inst if self.log_stack else False, depth=2)
        lg.log(self.level, msg_str)

        if self.debug_stack:
            logger.opt(exception=exc_inst, depth=2).debug("Stacktrace")

        return True


warning_suppress = partial(
    logged_suppress,
    level="WARNING",
    log_stack=False,
    debug_stack=True,
    append_exc_msg=True,
)
