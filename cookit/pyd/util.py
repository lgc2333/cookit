from typing import Callable, TypeVar, cast
from typing_extensions import TypeAlias

from pydantic import BaseModel, ConfigDict

from .compat import get_model_with_config

TTM = TypeVar("TTM", bound=type[BaseModel])
AliasFuncType: TypeAlias = Callable[[str], str]


def model_with_model_config(config: ConfigDict) -> Callable[[TTM], TTM]:
    def wrapper(base: TTM) -> TTM:
        m = get_model_with_config(config, base)
        return cast("TTM", m)

    return wrapper


def model_with_alias_generator(alias_func: AliasFuncType) -> Callable[[TTM], TTM]:
    def wrapper(base: TTM) -> TTM:
        config = ConfigDict(alias_generator=alias_func)
        m = get_model_with_config(config, base)
        return cast("TTM", m)

    return wrapper
