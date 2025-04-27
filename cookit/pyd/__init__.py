"""Install `cookit[pydantic]` before import this module."""

from .compat import (
    PYDANTIC_V2 as PYDANTIC_V2,
    field_validator as field_validator,
    get_model_with_config as get_model_with_config,
    model_config as model_config,
    model_copy as model_copy,
    model_dump as model_dump,
    model_validator as model_validator,
    type_dump_json as type_dump_json,
    type_dump_python as type_dump_python,
    type_validate_json as type_validate_json,
    type_validate_python as type_validate_python,
)
from .deprecated import (
    CamelAliasModel as CamelAliasModel,
    get_alias_model as get_alias_model,
)
from .util import (
    AliasFuncType as AliasFuncType,
    model_with_alias_generator as model_with_alias_generator,
    model_with_model_config as model_with_model_config,
)
