from typing import Callable, Type
from typing_extensions import TypeAlias

from pydantic import BaseModel, ConfigDict

from .. import camel_case
from .compat import get_model_with_config

AliasFuncType: TypeAlias = Callable[[str], str]


def get_alias_model(alias_func: AliasFuncType) -> Type[BaseModel]:
    return get_model_with_config(ConfigDict(alias_generator=alias_func))


CamelAliasModel = get_alias_model(camel_case)
