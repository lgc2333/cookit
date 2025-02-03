from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
    TypeVar,
    Union,
    overload,
)

from pydantic import VERSION, BaseModel, ConfigDict

PYDANTIC_V2 = int(VERSION.split(".", 1)[0]) == 2

T = TypeVar("T")


if PYDANTIC_V2:  # pragma: pydantic-v2
    from pydantic import (
        RootModel,
        TypeAdapter,
        field_validator as field_validator,
        model_validator as model_validator,
    )

    # region from nonebot2

    def model_config(model: type[BaseModel]) -> ConfigDict:
        """Get config of a model."""
        return model.model_config

    def model_dump(
        model: BaseModel,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        return model.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def type_validate_python(type_: type[T], data: Any) -> T:
        """Validate data with given type."""
        return (
            type_.model_validate(data)
            if type_ is BaseModel
            else TypeAdapter(type_).validate_python(data)
        )

    def type_validate_json(type_: type[T], data: Union[str, bytes]) -> T:
        """Validate JSON with given type."""
        return (
            type_.model_validate_json(data)
            if type_ is BaseModel
            else TypeAdapter(type_).validate_json(data)
        )

    # endregion

    def get_model_with_config(config: ConfigDict) -> type[BaseModel]:
        class Model(BaseModel):
            model_config = config

        return Model

    def __get_model_instance(data: object) -> BaseModel:
        return (
            data if isinstance(data, BaseModel) else RootModel(Any).model_validate(data)
        )

    def type_dump_python(
        data: object,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Any:
        return __get_model_instance(data).model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def type_dump_json(
        data: object,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> str:
        return __get_model_instance(data).model_dump_json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )


else:  # pragma: pydantic-v1
    from pydantic import parse_obj_as, parse_raw_as, root_validator, validator

    if TYPE_CHECKING:
        from pydantic import _V2BeforeAfterOrPlainValidatorType, _V2WrapValidatorType

    # region from nonebot2

    def model_config(model: type[BaseModel]) -> ConfigDict:
        """Get config of a model."""
        return (
            model.__config__
            if isinstance(model.__config__, dict)
            else ConfigDict(
                {
                    k: v
                    for k, v in model.__config__.__dict__.items()
                    if not (k.startswith("__") and k.endswith("__"))
                },
            )
        )

    def model_dump(
        model: BaseModel,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        return model.dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def type_validate_python(type_: type[T], data: Any) -> T:
        """Validate data with given type."""
        return parse_obj_as(type_, data)

    def type_validate_json(type_: type[T], data: Union[str, bytes]) -> T:
        """Validate JSON with given type."""
        return parse_raw_as(type_, data)

    # endregion

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
        __field: str,  # noqa: PYI063
        *fields: str,
        mode: Literal["before", "after", "plain"] = ...,
        check_fields: Optional[bool] = ...,
    ) -> Callable[
        ["_V2BeforeAfterOrPlainValidatorType"],
        "_V2BeforeAfterOrPlainValidatorType",
    ]: ...

    @overload
    def field_validator(
        __field: str,  # noqa: PYI063
        *fields: str,
        mode: Literal["wrap"],
        check_fields: Optional[bool] = ...,
    ) -> Callable[["_V2WrapValidatorType"], "_V2WrapValidatorType"]: ...

    def field_validator(
        __field: str,  # noqa: PYI063
        *fields: str,
        mode: Literal["before", "after", "wrap", "plain"] = "after",
        check_fields: Optional[bool] = None,  # noqa: ARG001
    ):
        return validator(__field, *fields, pre=(mode == "before"), allow_reuse=True)

    def get_model_with_config(config: ConfigDict) -> type[BaseModel]:
        class Model(BaseModel, **config):
            pass

        return Model

    class AnyRootModel(BaseModel):
        __root__: Any

    def __get_model_instance(data: object) -> BaseModel:
        return data if isinstance(data, BaseModel) else AnyRootModel.parse_obj(data)

    def type_dump_python(
        data: object,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Any:
        dumped = __get_model_instance(data).dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        if "__root__" in dumped:
            return dumped["__root__"]
        return dumped

    def type_dump_json(
        data: object,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Any:
        return __get_model_instance(data).json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
