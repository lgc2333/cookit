from typing_extensions import deprecated

from pydantic import BaseModel, ConfigDict

from .. import camel_case
from .compat import get_model_with_config
from .util import AliasFuncType, model_with_alias_generator


@deprecated("Use `model_with_alias_generator` instead.")
def get_alias_model(alias_func: AliasFuncType) -> type[BaseModel]:
    return get_model_with_config(ConfigDict(alias_generator=alias_func))


@deprecated("Use `model_with_alias_generator` instead.")
@model_with_alias_generator(camel_case)
class CamelAliasModel(BaseModel):
    pass
