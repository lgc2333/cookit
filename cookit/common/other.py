import asyncio
from asyncio import Semaphore
from typing import Any, Awaitable, Callable, Coroutine, TypeVar
from typing_extensions import ParamSpec

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")


def with_semaphore(semaphore: Semaphore):
    def decorator(func: Callable[P, Awaitable[R]]):
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    return decorator


def queued(func: Callable[P, Awaitable[R]]):
    return with_semaphore(Semaphore(1))(func)


async def race(*coros: Coroutine[Any, Any, T]) -> T:
    done, pending = await asyncio.wait(
        [asyncio.create_task(x) for x in coros],
        return_when=asyncio.FIRST_COMPLETED,
    )
    first, *other = done
    for t in (*other, *pending):
        t.cancel()
    return first.result()
