import pytest

from .utils import test_logger


def test_logged_suppress():
    from cookit.loguru import logged_suppress

    def value_error():
        raise ValueError("val")

    def index_error():
        raise IndexError

    with test_logger() as ctx:
        with logged_suppress("test1"):
            value_error()
        ctx.should_message("test1")

        with logged_suppress("test2", ValueError):
            value_error()
        ctx.should_message("test2")

        try:
            with logged_suppress("test3", ValueError):
                index_error()
        except IndexError:
            pass
        else:
            pytest.fail("IndexError should be raised")

        with logged_suppress(lambda e: f"test4: {e.args[0]}", ValueError, IndexError):
            value_error()
        ctx.should_message("test4: val")

        with logged_suppress(
            lambda e: f"test5: {type(e).__name__}",
            ValueError,
            IndexError,
        ):
            index_error()
        ctx.should_message("test5: IndexError")
