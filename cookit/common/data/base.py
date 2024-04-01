from typing import Callable, Dict, Iterable, Iterator, List, Sequence, TypeVar, Union
from typing_extensions import TypeGuard

T = TypeVar("T")

TA = TypeVar("TA")
TB = TypeVar("TB")
N = TypeVar("N")

K = TypeVar("K")
V = TypeVar("V")


def qor(
    a: Union[TA, N],
    b: Union[TB, Callable[[], TB]],
    none_val: N = None,
) -> Union[TA, TB]:
    def guard(x: Union[TA, N]) -> TypeGuard[TA]:
        return x is not none_val

    return a if guard(a) else (b() if isinstance(b, Callable) else b)


def chunks(lst: Sequence[T], n: int) -> Iterator[Sequence[T]]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def flatten(li: Iterable[Iterable[T]]) -> List[T]:
    return [x for y in li for x in y]


def set_default(target: Dict[K, V], key: K, default: Union[V, Callable[[], V]]) -> V:
    if key in target:
        return target[key]
    if callable(default):
        default = default()
    target[key] = default
    return default
