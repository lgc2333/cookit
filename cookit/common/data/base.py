import base64
from contextlib import suppress
from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Sequence,
    TypeVar,
    Union,
    cast,
    overload,
)
from typing_extensions import ParamSpec, TypeGuard

import fleep

T = TypeVar("T")

TA = TypeVar("TA")
TB = TypeVar("TB")
N = TypeVar("N")

K = TypeVar("K")
V = TypeVar("V")

P = ParamSpec("P")
R = TypeVar("R")

LazyGetterType = Union[T, Callable[P, T]]


def lazy_get(
    val: "LazyGetterType[T, P]",
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    return val(*args, **kwargs) if callable(val) else val


def qor(
    a: Union[TA, N],
    b: "LazyGetterType[TB, []]",
    none_val: N = None,
) -> Union[TA, TB]:
    def guard(x: Union[TA, N]) -> TypeGuard[TA]:
        return x is not none_val

    return a if guard(a) else lazy_get(b)


def chunks(lst: Sequence[T], n: int) -> Iterator[Sequence[T]]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def flatten(li: Iterable[Iterable[T]]) -> List[T]:
    return [x for y in li for x in y]


def set_default(target: Dict[K, V], key: K, default: "LazyGetterType[V, []]") -> V:
    if key in target:
        return target[key]
    default = lazy_get(default)
    target[key] = default
    return default


@overload
def auto_delete(target: Dict[K, V], transform: Literal[None] = None) -> Dict[K, V]: ...
@overload
def auto_delete(
    target: Dict[K, V],
    transform: Callable[[V], Optional[T]],
) -> Dict[K, T]: ...
def auto_delete(  # noqa: E302
    target: Dict[K, V],
    transform: Optional[Callable[[V], Optional[T]]] = None,
) -> Dict[K, Any]:
    data: Dict[K, Union[V, T]] = {}
    for k, v in tuple(target.items()):
        vt = transform(v) if transform else v
        if vt:
            data[k] = vt
        else:  # expected behavior, bool(vt) == False will be removed
            del target[k]
    return data


def to_b64_url(data: bytes, mime: Optional[str] = None) -> str:
    if mime is None:
        with suppress(IndexError):
            mime = cast(List[str], fleep.get(data[:128]).mime)[0]
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


@overload
def append_func_to_dict_deco(
    name_dict: Dict[str, Callable],
    func_or_name: Callable[P, R],
) -> Callable[P, R]: ...
@overload
def append_func_to_dict_deco(
    name_dict: Dict[str, Callable],
    func_or_name: str,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
def append_func_to_dict_deco(
    name_dict: Dict[str, Callable],
    func_or_name: Union[Callable[P, R], str],
):
    if callable(func_or_name):
        name_dict[func_or_name.__name__] = func_or_name
        return func_or_name

    def inner_deco(func: Callable[P, R], /):
        name_dict[func_or_name] = func
        return func

    return inner_deco


def make_append_func_to_dict_deco(name_dict: Dict[str, Callable]):
    return partial(append_func_to_dict_deco, name_dict)
