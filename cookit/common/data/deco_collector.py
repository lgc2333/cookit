from typing import Callable, Generic, Optional, Protocol, TypeVar, Union, overload
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
        data: Optional[dict[K, V]] = None,
        allow_overwrite: bool = False,
    ) -> None:
        super().__init__()
        self.data: dict[K, V] = {} if data is None else data
        self.allow_overwrite = allow_overwrite

    def set_data_item(self, key: K, value: V, /) -> None:
        if (not self.allow_overwrite) and (key in self.data):
            raise ValueError(f"Object with key '{key}' already exists")
        self.data[key] = value

    def __call__(self, key: K) -> Callable[[V], V]:
        def deco(obj: V) -> V:
            self.set_data_item(key, obj)
            return obj

        return deco


class TypeDecoCollector(DecoCollector[type[K], V]):
    @overload
    def get_from_type_or_instance(self, obj: Union[type[K], K]) -> V: ...
    @overload
    def get_from_type_or_instance(
        self,
        obj: Union[type[K], K],
        default: T = ...,
    ) -> Union[V, T]: ...
    def get_from_type_or_instance(
        self,
        obj: Union[type[K], K],
        default: T = ...,
    ) -> Union[V, T]:
        type_key: type[K] = obj if isinstance(obj, type) else type(obj)
        try:
            return self.data[type_key]
        except KeyError:
            if default is ...:
                raise
            return default


class NameDecoCollector(DecoCollector[str, Union[T_HasName]]):
    @overload
    def __call__(self, key: str) -> Callable[[T_HasName], T_HasName]: ...
    @overload
    def __call__(self, key: T_HasName) -> T_HasName: ...
    @override
    def __call__(self, key: Union[str, T_HasName]):  # type: ignore[reportIncompatibleMethodOverride]
        if isinstance(key, str):
            return super().__call__(key)
        if isinstance((name := getattr(key, "__name__", None)), str):
            return super().__call__(name)(key)
        raise TypeError("'key' must be str or object with __name__ attribute")


class DecoListCollector(Generic[T]):
    def __init__(self, data: Optional[list[T]] = None) -> None:
        super().__init__()
        self.data: list[T] = [] if data is None else data

    def __call__(self, obj: T) -> T:
        self.data.append(obj)
        return obj
