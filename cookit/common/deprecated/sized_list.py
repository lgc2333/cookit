from collections.abc import Iterable
from typing import Generic, SupportsIndex, TypeVar, overload
from typing_extensions import Self, deprecated

T = TypeVar("T")
TB = TypeVar("TB")


@deprecated("Use `collections.deque` instead")
class SizedList(list[T], Generic[T]):
    def __init__(
        self,
        iterable: Iterable[T] | None = None,
        size: int | None = None,
    ) -> None:
        if iterable is None:
            super().__init__()
        else:
            super().__init__(iterable)
        self.size = size
        self._handle_overflow()

    @property
    def last(self) -> T | None:
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
    def __add__(self, items: Iterable[TB]) -> "SizedList[T | TB]": ...

    def __add__(self, items):
        return SizedList((*self, *items), size=self.size)

    def __iadd__(self, items: Iterable[T]) -> Self:
        self.extend(items)
        return self
