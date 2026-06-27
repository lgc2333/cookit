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
        """Create a list that keeps only the newest items within a size limit."""
        if iterable is None:
            super().__init__()
        else:
            super().__init__(iterable)
        self.size = size
        self._handle_overflow()

    @property
    def last(self) -> T | None:
        """Return the last item if the list is not empty."""
        if self:
            return self[-1]
        return None

    def _handle_overflow(self) -> None:
        """Trim leading items until the list fits the configured size."""
        if self.size is None:
            return
        while len(self) > self.size:
            self.pop(0)

    def append(self, item: T) -> None:
        """Append an item and trim overflow."""
        super().append(item)
        self._handle_overflow()

    def extend(self, items: Iterable[T]) -> None:
        """Extend the list and trim overflow."""
        super().extend(items)
        self._handle_overflow()

    def insert(self, index: SupportsIndex, item: T) -> None:
        """Insert an item and trim overflow."""
        super().insert(index, item)
        self._handle_overflow()

    @overload
    def __add__(self, items: Iterable[T]) -> "SizedList[T]":
        """Return a new sized list with additional compatible items."""

    @overload
    def __add__(self, items: Iterable[TB]) -> "SizedList[T | TB]":
        """Return a new sized list with additional mixed-type items."""

    def __add__(self, items):
        """Return a new sized list containing current and added items."""
        return SizedList((*self, *items), size=self.size)

    def __iadd__(self, items: Iterable[T]) -> Self:
        """Extend this sized list in place and return it."""
        self.extend(items)
        return self
