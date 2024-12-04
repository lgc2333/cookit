from collections.abc import MutableMapping
from typing import Any, Callable, TypeVar, overload
from typing_extensions import deprecated

from cookit.common import (
    HasNameProtocol,
    append_obj_to_dict_deco,
    make_append_obj_to_dict_deco,
)

T = TypeVar("T")
T_HasName = TypeVar("T_HasName", bound=HasNameProtocol)


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
@deprecated("Use `append_obj_to_dict_deco` instead")
def append_func_to_dict_deco(name_dict: Any, func_or_name: Any):
    return append_obj_to_dict_deco(name_dict, func_or_name)


@deprecated("Use `make_append_obj_to_dict_deco` instead")
def make_append_func_to_dict_deco(name_dict: dict[str, Callable]):
    return make_append_obj_to_dict_deco(name_dict)
