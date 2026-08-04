from pydantic import BaseModel, ConfigDict


def test_model_with_model_config():
    from cookit.pyd.compat import model_config
    from cookit.pyd.util import model_with_model_config

    # 创建一个测试配置
    test_config = ConfigDict(arbitrary_types_allowed=True)

    # 创建一个基础模型
    class TestModel(BaseModel):
        name: str
        age: int

    # 应用装饰器
    @model_with_model_config(test_config)
    class ConfiguredModel(TestModel):
        pass

    # 验证配置是否正确应用
    assert model_config(ConfiguredModel).get("arbitrary_types_allowed") is True

    # 验证模型功能是否正常
    model = ConfiguredModel(name="test", age=25)
    assert model.name == "test"
    assert model.age == 25

    # 验证原始模型的配置不受影响
    assert model_config(TestModel).get("arbitrary_types_allowed") is not True


def test_model_with_alias_generator():
    from cookit import camel_case
    from cookit.pyd.compat import type_dump_python, type_validate_python
    from cookit.pyd.util import model_with_alias_generator

    # 创建一个基础模型
    class TestModel(BaseModel):
        user_name: str
        user_age: int

    # 应用装饰器
    @model_with_alias_generator(camel_case)
    class AliasedModel(TestModel):
        pass

    # 验证别名是否正确应用
    model = type_validate_python(
        AliasedModel,
        {"userName": "test", "userAge": 25},
    )

    # 验证模型功能是否正常
    assert model.user_name == "test"
    assert model.user_age == 25

    # 验证别名是否正确生成
    model_dict = type_dump_python(model, by_alias=True)
    assert "userName" in model_dict
    assert "userAge" in model_dict
    assert model_dict["userName"] == "test"
    assert model_dict["userAge"] == 25

    # 验证原始模型的别名不受影响
    original_model = type_validate_python(
        TestModel,
        {"user_name": "test", "user_age": 25},
    )
    original_dict = type_dump_python(original_model, by_alias=True)
    assert "user_name" in original_dict
    assert "user_age" in original_dict
