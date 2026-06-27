from collections.abc import Callable
from typing import Generic, Protocol, TypeVar, overload
from typing_extensions import override

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class HasNameProtocol(Protocol):
    __name__: str


T_HasName = TypeVar("T_HasName", bound=HasNameProtocol)


class DecoCollector(Generic[K, V]):
    def __init__(
        self,
        data: dict[K, V] | None = None,
        allow_overwrite: bool = False,
    ) -> None:
        """Create a decorator-backed dictionary collector."""
        super().__init__()
        self.data: dict[K, V] = {} if data is None else data
        self.allow_overwrite = allow_overwrite

    def set_data_item(self, key: K, value: V, /) -> None:
        """Store a collected value under a key, respecting overwrite rules."""
        if (not self.allow_overwrite) and (key in self.data):
            raise ValueError(f"Object with key '{key}' already exists")
        self.data[key] = value

    def __call__(self, key: K) -> Callable[[V], V]:
        """Create a decorator that collects an object under the given key."""

        def deco(obj: V) -> V:
            self.set_data_item(key, obj)
            return obj

        return deco


class TypeDecoCollector(DecoCollector[type[K], V]):
    @overload
    def get_from_type_or_instance(self, obj: type[K] | K) -> V:
        """Fetch collected data by a type or by an instance's type."""

    @overload
    def get_from_type_or_instance(
        self,
        obj: type[K] | K,
        default: T = ...,
    ) -> V | T:
        """Fetch collected data by type, returning a default if missing."""

    def get_from_type_or_instance(
        self,
        obj: type[K] | K,
        default: T = ...,
    ) -> V | T:
        """Fetch collected data using either a class or an object's class."""
        type_key: type[K] = obj if isinstance(obj, type) else type(obj)
        try:
            return self.data[type_key]
        except KeyError:
            if default is ...:
                raise
            return default


class NameDecoCollector(DecoCollector[str, T_HasName]):
    @overload
    def __call__(self, key: str) -> Callable[[T_HasName], T_HasName]:
        """Create a decorator that collects an object under a name."""

    @overload
    def __call__(self, key: T_HasName) -> T_HasName:
        """Collect a named object under its __name__."""

    @override
    def __call__(self, key: str | T_HasName):  # type: ignore[reportIncompatibleMethodOverride]
        """Collect by explicit name or by an object's __name__ attribute."""
        if isinstance(key, str):
            return super().__call__(key)
        if isinstance((name := getattr(key, "__name__", None)), str):
            return super().__call__(name)(key)
        raise TypeError("'key' must be str or object with __name__ attribute")


class DecoListCollector(Generic[T]):
    def __init__(self, data: list[T] | None = None) -> None:
        """Create a decorator-backed list collector."""
        super().__init__()
        self.data: list[T] = [] if data is None else data

    def __call__(self, obj: T) -> T:
        """Append the decorated object to the collector list."""
        self.data.append(obj)
        return obj
