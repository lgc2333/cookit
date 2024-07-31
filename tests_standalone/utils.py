import asyncio
from asyncio import Semaphore
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Awaitable, Callable, List, Optional, Type, TypeVar
from typing_extensions import TypeAlias

from loguru import logger

TestFunc: TypeAlias = Callable[[], Awaitable[Any]]

T = TypeVar("T")
TF = TypeVar("TF", bound=TestFunc)

tests: List[TestFunc] = []
before_exit_hooks: List[TestFunc] = []


def mark_test(func: TF) -> TF:
    tests.append(func)
    return func


def mark_before_exit(func: TF) -> TF:
    before_exit_hooks.append(func)
    return func


def wrapper_log(func: TestFunc) -> TestFunc:
    async def wrapper():
        logger.opt(colors=True).info(f"Running test <y>{func.__name__}</y>")
        try:
            return await func()
        except Exception:
            logger.exception(f"Test {func.__name__} failed")
            raise

    return wrapper


async def run_tests():
    from cookit import with_semaphore

    try:
        sem = Semaphore(8)
        await asyncio.gather(
            *(
                with_semaphore(sem)(
                    wrapper_log(x),
                )()
                for x in tests
            ),
        )
    except Exception:  # noqa: S110
        pass
    else:
        logger.success("All tests passed")
    finally:
        end_sem = Semaphore(8)
        await asyncio.gather(
            *(
                with_semaphore(end_sem)(
                    logger.catch(
                        message=f"Before exit hook {x.__name__} raised exception",
                    )(x),
                )()
                for x in before_exit_hooks
            ),
        )


def auto_import_tests(path: str, package: Optional[str]):
    from cookit import auto_import

    auto_import(
        Path(path).parent,
        package,
        lambda x: x.is_dir() or x.name.startswith("test_"),
    )


@contextmanager
def expect_exc(*exc: Type[BaseException]):
    try:
        yield
    except exc:
        return
    raise AssertionError
