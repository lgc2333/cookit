from asyncio import Semaphore
from typing import Awaitable, Callable, TypeVar
from typing_extensions import ParamSpec

R = TypeVar("R")
P = ParamSpec("P")


def with_semaphore(semaphore: Semaphore):
    def decorator(func: Callable[P, Awaitable[R]]):
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    return decorator
