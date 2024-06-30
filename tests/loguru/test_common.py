import pytest

from .utils import LoggingContext


def test_logged_suppress():
    from cookit.loguru import logged_suppress

    def value_error():
        raise ValueError("val")

    def index_error():
        raise IndexError

    with LoggingContext() as ctx:
        with logged_suppress("test1"):
            value_error()
        ctx.should_log(message="test1", level_str="ERROR", exception=ValueError)

        with logged_suppress("test2", ValueError):
            value_error()
        ctx.should_log(message="test2", level_str="ERROR", exception=ValueError)

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
        )

        with logged_suppress("test6", log_stack=False, debug_stack=True):
            value_error()
        ctx.should_log(message="test6", level_str="ERROR", exception=None)
        ctx.should_log(message="Stacktrace", level_str="DEBUG", exception=ValueError)
