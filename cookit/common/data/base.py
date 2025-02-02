import base64
from collections.abc import Iterable, Iterator, Sequence
from contextlib import suppress
from typing import Any, Callable, Optional, TypeVar, Union, cast, overload
from typing_extensions import ParamSpec, TypeGuard

T = TypeVar("T")

TA = TypeVar("TA")
TB = TypeVar("TB")
N = TypeVar("N")

K = TypeVar("K")
V = TypeVar("V")

P = ParamSpec("P")

LazyGetterType = Union[T, Callable[P, T]]


def lazy_get(
    val: "LazyGetterType[T, P]",
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    return cast("T", val(*args, **kwargs) if callable(val) else val)


def qor(
    a: Union[TA, N],
    b: "LazyGetterType[TB, []]",
    none_val: N = None,
) -> Union[TA, TB]:
    def guard(x: Union[TA, N]) -> TypeGuard[TA]:
        return x is not none_val

    return a if guard(a) else lazy_get(b)


def chunks(lst: Sequence[T], n: int) -> Iterator[list[T]]:
    for i in range(0, len(lst), n):
        yield list(lst[i : i + n])


def flatten(li: Iterable[Iterable[T]]) -> list[T]:
    return [x for y in li for x in y]


def set_default(target: dict[K, V], key: K, default: "LazyGetterType[V, []]") -> V:
    if key in target:
        return target[key]
    default = lazy_get(default)
    target[key] = default
    return default


@overload
def auto_delete(target: dict[K, V], transform: None = None) -> dict[K, V]: ...
@overload
def auto_delete(
    target: dict[K, V],
    transform: Callable[[V], Optional[T]],
) -> dict[K, T]: ...
def auto_delete(  # noqa: E302
    target: dict[K, V],
    transform: Optional[Callable[[V], Optional[T]]] = None,
) -> dict[K, Any]:
    data: dict[K, Union[V, T]] = {}
    for k, v in tuple(target.items()):
        vt = transform(v) if transform else v
        if vt:
            data[k] = vt
        else:  # expected behavior, bool(vt) == False will be removed
            del target[k]
    return data


def to_b64_url(data: bytes, mime: Optional[str] = None) -> str:
    if mime is None:
        mime = ""
        with suppress(ImportError, IndexError):
            import fleep

            mime = cast("list[str]", fleep.get(data[:128]).mime)[0]

    return f"data:{mime};base64,{base64.b64encode(data).decode()}"
