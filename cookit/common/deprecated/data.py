from collections.abc import MutableMapping
from functools import partial
from typing import Any, Callable, Generic, Protocol, TypeVar, Union, overload
from typing_extensions import deprecated

from cookit.common import HasNameProtocol

T = TypeVar("T")
T_HasName = TypeVar("T_HasName", bound=HasNameProtocol)


@overload
def append_obj_to_dict_deco(
    name_dict: MutableMapping[str, T_HasName],
    obj_or_name: T_HasName,
    allow_overwrite: bool = True,
) -> T_HasName: ...
@overload
def append_obj_to_dict_deco(
    name_dict: MutableMapping[str, T],
    obj_or_name: str,
    allow_overwrite: bool = True,
) -> Callable[[T], T]: ...
@deprecated("Use `NameDecoCollector` instead")
def append_obj_to_dict_deco(  # type: ignore
    name_dict: MutableMapping[str, T],
    obj_or_name: Union[str, T],
    allow_overwrite: bool = True,
):
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
    def __call__(self, x: T) -> T: ...
    @overload
    def __call__(self, x: str) -> Callable[[T], T]: ...


@overload
def make_append_obj_to_dict_deco(
    name_dict: MutableMapping[str, T_HasName],
    allow_overwrite: bool = True,
) -> AppendObjDecoProtocol[T_HasName]: ...
@overload
def make_append_obj_to_dict_deco(
    name_dict: MutableMapping[str, T],
    allow_overwrite: bool = True,
) -> Callable[[str], Callable[[T], T]]: ...
@deprecated("Use `NameDecoCollector` instead")
def make_append_obj_to_dict_deco(name_dict: MutableMapping[str, Any], **kwargs):  # type: ignore
    return partial(append_obj_to_dict_deco, name_dict, **kwargs)


@overload
def append_func_to_dict_deco(
    name_dict: MutableMapping[str, T_HasName],
    func_or_name: T_HasName,
) -> T_HasName: ...
@overload
def append_func_to_dict_deco(
    name_dict: MutableMapping[str, T],
    func_or_name: str,
) -> Callable[[T], T]: ...
@deprecated("Use `NameDecoCollector` instead")
def append_func_to_dict_deco(name_dict: Any, func_or_name: Any):
    return append_obj_to_dict_deco(name_dict, func_or_name)


@deprecated("Use `NameDecoCollector` instead")
def make_append_func_to_dict_deco(name_dict: dict[str, Callable]):
    return make_append_obj_to_dict_deco(name_dict)
