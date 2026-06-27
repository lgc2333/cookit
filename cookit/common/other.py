import asyncio
import importlib
import sys
from asyncio import Semaphore, Task
from collections.abc import Awaitable, Callable, Coroutine
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar
from typing_extensions import ParamSpec, override

if TYPE_CHECKING:
    from types import ModuleType

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")
P2 = ParamSpec("P2")


def with_semaphore(semaphore: Semaphore):
    """Create a decorator that limits async function concurrency with a semaphore."""

    def decorator(func: Callable[P, Awaitable[R]]):
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    return decorator


def queued(func: Callable[P, Awaitable[R]]):
    """Serialize calls to an async function with a single-slot semaphore."""
    return with_semaphore(Semaphore(1))(func)


async def race(
    *coroutines: Coroutine[Any, Any, T] | Task[T],
    cancel: bool = True,
) -> T:
    """Return the first completed coroutine result and optionally cancel the rest."""
    done, pending = await asyncio.wait(
        [(x if isinstance(x, Task) else asyncio.create_task(x)) for x in coroutines],
        return_when=asyncio.FIRST_COMPLETED,
    )
    first, *other = done
    if cancel:
        for t in (*other, *pending):
            t.cancel()
    return first.result()


def auto_import(
    path: str | Path,
    package: str | None = None,
    path_filter: Callable[[Path], bool] | None = None,
):
    """Import all visible Python modules or packages in a directory."""
    if not isinstance(path, Path):
        path = Path(path)
    if not path_filter:
        path_filter = lambda x: not x.name.startswith("_")  # noqa: E731

    modules: list[ModuleType] = []
    for p in path.iterdir():
        if (
            (not (p / "__init__.py").exists()) if p.is_dir() else (p.suffix != ".py")
        ) or (not path_filter(p)):
            continue

        p = importlib.import_module(f".{p.stem}", package)
        assert p
        modules.append(p)

    return modules


if sys.version_info >= (3, 11):
    from enum import StrEnum as StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        @override
        @staticmethod
        def _generate_next_value_(
            name: str,
            start: int,
            count: int,
            last_values: list[str],
        ):
            """Use lowercase enum member names as automatic string values."""
            return name.lower()


# https://stackoverflow.com/questions/71968447/python-typing-copy-kwargs-from-one-function-to-another
def copy_func_annotations(_source: Callable[P, T]):
    """Copy a callable's full type signature onto another callable for typing."""

    def deco(func: Callable[..., T]) -> Callable[P, T]:
        return func

    return deco


def copy_func_arg_annotations(_source: Callable[P, Any]):
    """Copy a callable's argument annotations onto another callable for typing."""

    def deco(func: Callable[..., T]) -> Callable[P, T]:
        return func

    return deco
