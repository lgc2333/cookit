import pytest
from pydantic import BaseModel

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


def test_get_alias_model_creates_alias_generator_model():
    from cookit import camel_case
    from cookit.pyd import get_alias_model, type_dump_python, type_validate_python

    class UserModel(get_alias_model(camel_case)):
        user_name: str

    model = type_validate_python(UserModel, {"userName": "alice"})

    assert model.user_name == "alice"
    assert type_dump_python(model, by_alias=True) == {"userName": "alice"}


def test_camel_alias_model_uses_camel_case_aliases():
    from cookit.pyd import CamelAliasModel, type_dump_python, type_validate_python

    class UserModel(CamelAliasModel):
        user_name: str

    model = type_validate_python(UserModel, {"userName": "alice"})

    assert isinstance(model, BaseModel)
    assert model.user_name == "alice"
    assert type_dump_python(model, by_alias=True) == {"userName": "alice"}
