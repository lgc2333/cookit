import asyncio
from collections.abc import Callable, Coroutine
from typing import Any, Generic, NoReturn, TypeAlias, TypeVar
from typing_extensions import ParamSpec, Self

T = TypeVar("T")

Co: TypeAlias = Coroutine[Any, Any, T]

A = ParamSpec("A")
R = TypeVar("R")
E = TypeVar("E")


async def default_exc_handler(_: "Signal", e: Exception) -> NoReturn:
    raise e


async def safe_exc_handler(_: "Signal", e: Exception) -> Exception:
    return e


class Signal(Generic[A, R, E]):
    def __init__(
        self,
        exc_handler: Callable[[Self, Exception], Co[E]] = default_exc_handler,
    ) -> None:
        self.slots: list[Callable[A, Co[R]]] = []
        self.exc_handler = exc_handler

    def connect(self, slot: Callable[A, Co[R]]) -> Callable[A, Co[R]]:
        self.slots.append(slot)
        return slot

    async def run(
        self,
        func: Callable[A, Co[R]],
        *args: A.args,
        **kwargs: A.kwargs,
    ) -> R | E:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return await self.exc_handler(self, e)

    async def sequential(
        self,
        *args: A.args,
        **kwargs: A.kwargs,
    ) -> list[R | E]:
        return [await self.run(slot, *args, **kwargs) for slot in self.slots]

    def task_sequential(
        self,
        *args: A.args,
        **kwargs: A.kwargs,
    ) -> asyncio.Task[list[R | E]]:
        return asyncio.create_task(self.sequential(*args, **kwargs))

    async def gather(self, *args: A.args, **kwargs: A.kwargs) -> list[R | E]:
        return await asyncio.gather(
            *(self.run(slot, *args, **kwargs) for slot in self.slots),
        )

    def task_gather(
        self,
        *args: A.args,
        **kwargs: A.kwargs,
    ) -> asyncio.Task[list[R | E]]:
        return asyncio.create_task(self.gather(*args, **kwargs))
