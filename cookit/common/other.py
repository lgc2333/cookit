import asyncio
import importlib
from asyncio import Semaphore
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Coroutine,
    List,
    Optional,
    TypeVar,
    Union,
)
from typing_extensions import ParamSpec

if TYPE_CHECKING:
    from types import ModuleType

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


def auto_import(
    path: Union[str, Path],
    package: Optional[str] = None,
    path_filter: Optional[Callable[[Path], bool]] = None,
):
    if not isinstance(path, Path):
        path = Path(path)
    if not path_filter:
        path_filter = lambda x: not x.name.startswith("_")  # noqa: E731

    modules: List[ModuleType] = []
    for p in path.iterdir():
        if (
            (not (p / "__init__.py").exists()) if p.is_dir() else (p.suffix != ".py")
        ) or (not path_filter(p)):
            continue

        p = importlib.import_module(f".{p.stem}", package)
        assert p
        modules.append(p)

    return modules
