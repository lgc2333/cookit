from typing import Any

import pytest
from loguru import logger

from .utils import LoggingContext


def test_logged_suppress():
    from cookit.loguru import logged_suppress, warning_suppress

    def value_error():
        raise ValueError("val")

    def index_error():
        raise IndexError

    call_stack_check_kw: dict[str, Any] = {
        "name": "tests",
        "function": "test_logged_suppress",
    }

    with LoggingContext() as ctx:
        logger.info("test")
        ctx.should_log(
            message="test",
            level_str="INFO",
            **call_stack_check_kw,
        )

        with logged_suppress("test1"):
            value_error()
        ctx.should_log(
            message="test1",
            level_str="ERROR",
            exception=ValueError,
            **call_stack_check_kw,
        )

        with logged_suppress("test2", ValueError):
            value_error()
        ctx.should_log(
            message="test2",
            level_str="ERROR",
            exception=ValueError,
            **call_stack_check_kw,
        )

        try:
            with logged_suppress("test3", ValueError):
                index_error()
        except IndexError:
            pass
        else:
            pytest.fail("IndexError should be raised")

        with logged_suppress(
            lambda e: f"test4: {e.args[0]}",
            ValueError,
            IndexError,
            level="WARNING",
        ):
            value_error()
        ctx.should_log(
            message="test4: val",
            level_str="WARNING",
            exception=ValueError,
            **call_stack_check_kw,
        )

        with logged_suppress(
            lambda e: f"test5: {type(e).__name__}",
            ValueError,
            IndexError,
            level="DEBUG",
        ):
            index_error()
        ctx.should_log(
            message="test5: IndexError",
            level_str="DEBUG",
            exception=IndexError,
            **call_stack_check_kw,
        )

        with logged_suppress("test6", log_stack=False, debug_stack=True):
            value_error()
        ctx.should_log(
            message="test6",
            level_str="ERROR",
            exception=None,
            **call_stack_check_kw,
        )
        ctx.should_log(
            message="Stacktrace",
            level_str="DEBUG",
            exception=ValueError,
            **call_stack_check_kw,
        )

        with warning_suppress("test7"):
            value_error()
        ctx.should_log(
            message="test7: ValueError: val",
            level_str="WARNING",
            exception=None,
            **call_stack_check_kw,
        )
        ctx.should_log(
            message="Stacktrace",
            level_str="DEBUG",
            exception=ValueError,
            **call_stack_check_kw,
        )


def test_log_exception_warning():
    from cookit.loguru import log_exception_warning

    def value_error():
        raise ValueError("val")

    call_stack_check_kw: dict[str, Any] = {
        "name": "tests",
        "function": "test_log_exception_warning",
    }

    with LoggingContext() as ctx:
        try:
            value_error()
        except ValueError as e:
            log_exception_warning(e, "test1")
        ctx.should_log(
            message="test1: ValueError: val",
            level_str="WARNING",
            exception=None,
            **call_stack_check_kw,
        )
        ctx.should_log(
            message="Stacktrace",
            level_str="DEBUG",
            exception=ValueError,
            **call_stack_check_kw,
        )
