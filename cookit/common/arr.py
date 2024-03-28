from typing import (
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    SupportsIndex,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import Self, deprecated

T = TypeVar("T")
T2 = TypeVar("T2")


@deprecated("Use `collections.deque` instead")
class SizedList(Generic[T], List[T]):
    def __init__(
        self,
        iterable: Optional[Iterable[T]] = None,
        size: Optional[int] = None,
    ) -> None:
        if iterable is None:
            super().__init__()
        else:
            super().__init__(iterable)
        self.size = size
        self._handle_overflow()

    @property
    def last(self) -> Optional[T]:
        if self:
            return self[-1]
        return None

    def _handle_overflow(self) -> None:
        if self.size is None:
            return
        while len(self) > self.size:
            self.pop(0)

    def append(self, item: T) -> None:
        super().append(item)
        self._handle_overflow()

    def extend(self, items: Iterable[T]) -> None:
        super().extend(items)
        self._handle_overflow()

    def insert(self, index: SupportsIndex, item: T) -> None:
        super().insert(index, item)
        self._handle_overflow()

    @overload
    def __add__(self, items: Iterable[T]) -> "SizedList[T]": ...

    @overload
    def __add__(self, items: Iterable[T2]) -> "SizedList[Union[T, T2]]": ...

    def __add__(self, items):
        return SizedList((*self, *items), size=self.size)

    def __iadd__(self, items: Iterable[T]) -> Self:
        self.extend(items)
        return self


def chunks(lst: Sequence[T], n: int) -> Iterator[Sequence[T]]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def flatten(li: Iterable[Iterable[T]]) -> List[T]:
    return [x for y in li for x in y]
