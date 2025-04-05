from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
    Protocol,
    TypeVar,
    Union,
    overload,
)

from pydantic import VERSION, BaseModel, ConfigDict

# Reference: https://github.com/nonebot/nonebot2/blob/master/nonebot/compat.py

PYDANTIC_V2 = int(VERSION.split(".", 1)[0]) == 2

T = TypeVar("T")
TM = TypeVar("TM", bound=BaseModel)
TM_contra = TypeVar("TM_contra", bound=BaseModel, contravariant=True)


class FieldValidator(Protocol):
    def __call__(self, cls: Any, v: Any) -> Any: ...


class ModelBeforeValidator(Protocol):
    def __call__(self, cls: Any, values: Any) -> dict[str, Any]: ...


class ModelAfterValidator(Protocol):
    def __call__(self, cls: Any, values: dict[str, Any]) -> dict[str, Any]: ...


TFV = TypeVar("TFV", bound=FieldValidator)
TMBV = TypeVar("TMBV", bound=ModelBeforeValidator)
TMAV = TypeVar("TMAV", bound=ModelAfterValidator)


if PYDANTIC_V2:  # pragma: pydantic-v2
    from pydantic import (
        RootModel,
        TypeAdapter,
        field_validator as v2_field_validator,
        model_validator as v2_model_validator,
    )

    if TYPE_CHECKING:
        from pydantic.functional_validators import ModelWrapValidatorHandler

    def model_config(model: type[BaseModel]) -> ConfigDict:
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
        return (
            type_.model_validate(data)
            if type_ is BaseModel
            else TypeAdapter(type_).validate_python(data)
        )

    def type_validate_json(type_: type[T], data: Union[str, bytes]) -> T:
        return (
            type_.model_validate_json(data)
            if type_ is BaseModel
            else TypeAdapter(type_).validate_json(data)
        )

    @overload
    def model_validator(
        *,
        mode: Literal["before"],
    ) -> Callable[[TMBV], TMBV]: ...
    @overload
    def model_validator(
        *,
        mode: Literal["after"] = "after",
    ) -> Callable[[TMAV], TMAV]: ...
    def model_validator(
        *,
        mode: Literal["before", "after"] = "after",
    ) -> Callable[[Any], Any]:
        def deco(func: Any) -> Any:
            def wrapper(
                cls: type[BaseModel],
                data: Any,
                handler: "ModelWrapValidatorHandler[BaseModel]",
            ) -> Any:
                if mode == "before":
                    data = func(cls, data)
                validated = handler(data)
                if mode == "after":
                    values = {
                        x: getattr(validated, x) for x in validated.model_fields_set
                    }
                    updated = func(cls, values)
                    for k, v in updated.items():
                        setattr(validated, k, v)
                return validated

            return v2_model_validator(mode="wrap")(wrapper)

        return deco

    def field_validator(
        field: str,
        *fields: str,
        mode: Literal["before", "after"] = "after",
        check_fields: Optional[bool] = ...,
    ) -> Callable[[TFV], TFV]:
        return v2_field_validator(
            field,
            *fields,
            mode=mode,
            check_fields=check_fields if check_fields is not None else True,
        )

    def get_model_with_config(
        config: ConfigDict,
        base: type[BaseModel] = BaseModel,
        type_name: Optional[str] = None,
    ) -> type[BaseModel]:
        return type(type_name or base.__name__, (base,), {"model_config": config})

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

    def model_copy(
        model: TM,
        update: Optional[dict[str, Any]] = None,
        deep: bool = False,
    ) -> TM:
        return model.model_copy(update=update, deep=deep)


else:  # pragma: pydantic-v1
    from pydantic import parse_obj_as, parse_raw_as, root_validator, validator

    def model_config(model: type[BaseModel]) -> ConfigDict:
        return (
            model.__config__
            if isinstance(model.__config__, dict)
            else ConfigDict(
                {
                    k: v
                    for k, v in model.__config__.__dict__.items()
                    if not (k.startswith("__") and k.endswith("__"))
                },  # type: ignore
            )
        )  # type: ignore

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
        return parse_obj_as(type_, data)

    def type_validate_json(type_: type[T], data: Union[str, bytes]) -> T:
        return parse_raw_as(type_, data)  # type: ignore

    @overload
    def model_validator(
        *,
        mode: Literal["before"],
    ) -> Callable[[TMBV], TMBV]: ...
    @overload
    def model_validator(
        *,
        mode: Literal["after"] = "after",
    ) -> Callable[[TMAV], TMAV]: ...
    def model_validator(
        *,
        mode: Literal["before", "after"] = "after",
    ) -> Callable[[Any], Any]:
        return root_validator(pre=mode == "before", allow_reuse=True)

    def field_validator(
        field: str,
        *fields: str,
        mode: Literal["before", "after"] = "after",
        check_fields: Optional[bool] = ...,
    ) -> Callable[[TFV], TFV]:
        return validator(
            field,
            *fields,
            pre=(mode == "before"),
            allow_reuse=True,
            check_fields=check_fields if check_fields is not None else True,
        )

    def get_model_with_config(
        config: ConfigDict,
        base: type[BaseModel] = BaseModel,
        type_name: Optional[str] = None,
    ) -> type[BaseModel]:
        return type(type_name or base.__name__, (base,), {}, **config)

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

    def model_copy(
        model: TM,
        update: Optional[dict[str, Any]] = None,
        deep: bool = False,
    ) -> TM:
        return model.copy(update=update, deep=deep)
