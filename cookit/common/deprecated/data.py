from collections.abc import Callable, MutableMapping
from functools import partial
from typing import Any, Generic, Protocol, TypeVar, overload
from typing_extensions import deprecated

from cookit.common import HasNameProtocol

T = TypeVar("T")
T_HasName = TypeVar("T_HasName", bound=HasNameProtocol)


@overload
def append_obj_to_dict_deco(
    name_dict: MutableMapping[str, T_HasName],
    obj_or_name: T_HasName,
    allow_overwrite: bool = True,
) -> T_HasName:
    """Deprecated helper that stores a named object in a mapping."""


@overload
def append_obj_to_dict_deco(
    name_dict: MutableMapping[str, T],
    obj_or_name: str,
    allow_overwrite: bool = True,
) -> Callable[[T], T]:
    """Deprecated helper that creates a decorator to store objects in a mapping."""


@deprecated("Use `NameDecoCollector` instead")
def append_obj_to_dict_deco(  # type: ignore
    name_dict: MutableMapping[str, T],
    obj_or_name: str | T,
    allow_overwrite: bool = True,
):
    """Store an object in a mapping directly or through a name-based decorator."""

    def set_obj(name: str, obj: T) -> T:
        if (not allow_overwrite) and (name in name_dict):
            raise ValueError(f"Object with name '{name}' already exists")
        name_dict[name] = obj
        return obj

    if isinstance(obj_or_name, str):

        def inner_deco(obj: T, /):
            return set_obj(obj_or_name, obj)

        return inner_deco

    if isinstance(
        (name := getattr(obj_or_name, "__name__", None)),
        str,
    ):
        return set_obj(name, obj_or_name)

    raise TypeError("func_or_name must be str or object with __name__ attribute")


class AppendObjDecoProtocol(Protocol, Generic[T]):
    @overload
    def __call__(self, x: T) -> T:
        """Store a named object directly."""
        ...

    @overload
    def __call__(self, x: str) -> Callable[[T], T]:
        """Create a decorator that stores an object under a name."""
        ...


@overload
def make_append_obj_to_dict_deco(
    name_dict: MutableMapping[str, T_HasName],
    allow_overwrite: bool = True,
) -> AppendObjDecoProtocol[T_HasName]:
    """Deprecated factory for a named-object mapping decorator."""


@overload
def make_append_obj_to_dict_deco(
    name_dict: MutableMapping[str, T],
    allow_overwrite: bool = True,
) -> Callable[[str], Callable[[T], T]]:
    """Deprecated factory for an explicit-name mapping decorator."""


@deprecated("Use `NameDecoCollector` instead")
def make_append_obj_to_dict_deco(name_dict: MutableMapping[str, Any], **kwargs):  # type: ignore
    """Create a partial decorator that stores objects into a mapping."""
    return partial(append_obj_to_dict_deco, name_dict, **kwargs)


@overload
def append_func_to_dict_deco(
    name_dict: MutableMapping[str, T_HasName],
    func_or_name: T_HasName,
) -> T_HasName:
    """Deprecated helper that stores a named function in a mapping."""


@overload
def append_func_to_dict_deco(
    name_dict: MutableMapping[str, T],
    func_or_name: str,
) -> Callable[[T], T]:
    """Deprecated helper that creates a function-storing decorator."""


@deprecated("Use `NameDecoCollector` instead")
def append_func_to_dict_deco(name_dict: Any, func_or_name: Any):
    """Store a function in a mapping directly or through a decorator."""
    return append_obj_to_dict_deco(name_dict, func_or_name)


@deprecated("Use `NameDecoCollector` instead")
def make_append_func_to_dict_deco(name_dict: dict[str, Callable]):
    """Create a deprecated decorator that stores functions by name."""
    return make_append_obj_to_dict_deco(name_dict)
