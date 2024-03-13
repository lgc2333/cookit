from typing import TYPE_CHECKING, Callable, Literal, Optional, Type, overload
from typing_extensions import TypeAlias

from pydantic import VERSION, BaseModel

from .text import camel_case

PYDANTIC_V2 = int(VERSION.split(".", 1)[0]) == 2

AliasFuncType: TypeAlias = Callable[[str], str]

if PYDANTIC_V2:
    from pydantic import (
        ConfigDict,
        field_validator as field_validator,
        model_validator as model_validator,
    )

    def get_alias_model(alias_func: AliasFuncType) -> Type[BaseModel]:
        class Model(BaseModel):
            model_config = ConfigDict(alias_generator=alias_func)

        return Model


else:
    from pydantic import root_validator, validator

    if TYPE_CHECKING:
        from pydantic import _V2BeforeAfterOrPlainValidatorType, _V2WrapValidatorType

    @overload
    def model_validator(*, mode: Literal["before"]): ...

    @overload
    def model_validator(*, mode: Literal["after"]): ...

    def model_validator(*, mode: Literal["before", "after"]):
        return root_validator(
            pre=mode == "before",  # type: ignore
            allow_reuse=True,
        )

    @overload
    def field_validator(
        __field: str,
        *fields: str,
        mode: Literal["before", "after", "plain"] = ...,
        check_fields: Optional[bool] = ...,
    ) -> Callable[
        ["_V2BeforeAfterOrPlainValidatorType"],
        "_V2BeforeAfterOrPlainValidatorType",
    ]: ...

    @overload
    def field_validator(
        __field: str,
        *fields: str,
        mode: Literal["wrap"],
        check_fields: Optional[bool] = ...,
    ) -> Callable[["_V2WrapValidatorType"], "_V2WrapValidatorType"]: ...

    def field_validator(
        __field: str,
        *fields: str,
        mode: Literal["before", "after", "wrap", "plain"] = "after",
        check_fields: Optional[bool] = None,  # noqa: ARG001
    ):
        return validator(__field, *fields, pre=(mode == "before"), allow_reuse=True)

    def get_alias_model(alias_func: AliasFuncType) -> Type[BaseModel]:
        class Model(BaseModel):
            class Config:
                alias_generator = alias_func

        return Model


CamelAliasModel = get_alias_model(camel_case)
