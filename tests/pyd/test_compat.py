import json
from typing import Any, Optional

from cookit.pyd import (
    field_validator,
    get_model_with_config,
    model_config,
    model_copy,
    model_dump,
    model_validator,
    type_dump_json,
    type_dump_python,
    type_validate_json,
    type_validate_python,
)
from pydantic import BaseModel, ConfigDict

# region from nonebot2


def test_model_dump():
    class TestModel(BaseModel):
        test1: int
        test2: int

    assert model_dump(TestModel(test1=1, test2=2), include={"test1"}) == {"test1": 1}
    assert model_dump(TestModel(test1=1, test2=2), exclude={"test1"}) == {"test2": 2}

    class TestModelNested(BaseModel):
        nested: TestModel

    assert model_dump(TestModelNested(nested=TestModel(test1=1, test2=2))) == {
        "nested": {"test1": 1, "test2": 2},
    }


def test_validate():
    class TestModel(BaseModel):
        test1: int
        test2: str
        test3: bool
        test4: dict
        test5: list
        test6: Optional[int]

    data = {
        "test1": 1,
        "test2": "2",
        "test3": True,
        "test4": {},
        "test5": [],
        "test6": None,
    }
    expected = TestModel(test1=1, test2="2", test3=True, test4={}, test5=[], test6=None)
    assert type_validate_python(TestModel, data) == expected
    assert type_validate_json(TestModel, json.dumps(data)) == expected

    class TestModelNested(BaseModel):
        nested: TestModel

    data = {"nested": data}
    expected = TestModelNested(nested=expected)
    assert type_validate_python(TestModelNested, data) == expected


# endregion


def test_get_model_with_config():
    config = ConfigDict(arbitrary_types_allowed=True)
    TestModel1 = get_model_with_config(config)  # noqa: N806
    model1_ins = TestModel1()
    assert isinstance(model1_ins, TestModel1)
    assert isinstance(model1_ins, BaseModel)
    assert TestModel1.__name__ == "BaseModel"
    for k in config:
        assert model_config(TestModel1)[k] == config[k]

    class TestModel2(BaseModel):
        pass

    TestModel2New = get_model_with_config(config, base=TestModel2)  # noqa: N806
    model2_ins = TestModel2New()
    assert isinstance(model2_ins, TestModel2New)
    assert isinstance(model2_ins, TestModel2)
    assert isinstance(model1_ins, BaseModel)
    assert TestModel2New.__name__ == "TestModel2"
    for k in config:
        assert model_config(TestModel2New)[k] == config[k]

    TestModel3 = get_model_with_config(config, type_name="TestModel3")  # noqa: N806
    assert TestModel3.__name__ == "TestModel3"


def test_validate_root():
    from cookit.pyd import type_dump_json, type_dump_python

    class InnerTestModel(BaseModel):
        test31: int

    class TestModel(BaseModel):
        test1: int
        test2: str
        test3: InnerTestModel

    data = [{"test1": 1, "test2": "2", "test3": {"test31": 3}}]
    expected = [TestModel(test1=1, test2="2", test3=InnerTestModel(test31=3))]
    assert type_dump_python(expected) == data
    assert json.loads(type_dump_json(expected)) == data


def test_model_copy():
    class TestModel(BaseModel):
        test1: int
        test2: int

    model = TestModel(test1=1, test2=2)

    copied = model_copy(model)
    assert copied is not model
    assert copied == model

    # 测试更新字段
    copied_with_update = model_copy(model, update={"test1": 10})
    assert copied_with_update.test1 == 10
    assert copied_with_update.test2 == 2

    # 测试深拷贝
    class NestedModel(BaseModel):
        nested: dict[str, Any]

    nested_model = NestedModel(nested={"key": {"subkey": "value"}})
    shallow_copy = model_copy(nested_model)
    deep_copy = model_copy(nested_model, deep=True)

    # 修改原始对象中的嵌套字典
    nested_model.nested["key"]["subkey"] = "new_value"

    # 浅拷贝的嵌套字典应该被修改
    assert shallow_copy.nested["key"]["subkey"] == "new_value"
    # 深拷贝的嵌套字典不应该被修改
    assert deep_copy.nested["key"]["subkey"] == "value"


def test_field_validator():
    class TestModel(BaseModel):
        test1: int
        test2: str

        @field_validator("test1")
        def validate_test1(cls, v: int) -> int:  # noqa: N805
            return v * 2

        @field_validator("test2", mode="before")
        def validate_test2(cls, v: str) -> str:  # noqa: N805
            return str(v) + "_validated"

    model = TestModel(test1=5, test2="abc")
    assert model.test1 == 10  # 验证test1被乘以2
    assert model.test2 == "abc_validated"  # 验证test2被添加了后缀

    # 由于不同版本的Pydantic行为可能不同，我们分别测试
    class MultiFieldModelV1(BaseModel):
        field1: int
        field2: int

        @field_validator("field1")
        def validate_field1(cls, v: int) -> int:  # noqa: N805
            return v + 1

        @field_validator("field2")
        def validate_field2(cls, v: int) -> int:  # noqa: N805
            return v * 2

    multi_model = MultiFieldModelV1(field1=5, field2=5)
    assert multi_model.field1 == 6  # field1 + 1
    assert multi_model.field2 == 10  # field2 * 2


def test_model_validator():
    # 测试 before 模式
    class BeforeModel(BaseModel):
        x: int
        y: int

        @model_validator(mode="before")
        def validate_before(cls, values: Any):  # noqa: N805
            if isinstance(values, dict):
                values["x"] = values.get("x", 0) + 1
                values["y"] = values.get("y", 0) + 2
            return values

    before_model = BeforeModel(x=10, y=20)
    assert before_model.x == 11
    assert before_model.y == 22

    # 测试 after 模式
    class AfterModel(BaseModel):
        x: int
        y: int

        @model_validator(mode="after")
        def validate_after(cls, values: Any):  # noqa: N805
            values_copy = dict(values)
            values_copy["x"] = values["x"] * 2
            return values_copy

    after_model = AfterModel(x=10, y=20)
    assert after_model.x == 20  # x被乘以2
    assert after_model.y == 20  # y保持不变


def test_type_dump_python_advanced():
    # 测试各种类型的数据
    # 基本类型
    assert type_dump_python(5) == 5
    assert type_dump_python("test") == "test"
    assert type_dump_python(data=True) is True

    # 列表和字典
    assert type_dump_python([1, 2, 3]) == [1, 2, 3]
    assert type_dump_python({"a": 1, "b": 2}) == {"a": 1, "b": 2}

    # Pydantic模型
    class ComplexModel(BaseModel):
        int_val: int
        str_val: str
        list_val: list[int]
        dict_val: dict[str, Any]
        none_val: Optional[int] = None

    model = ComplexModel(
        int_val=1,
        str_val="test",
        list_val=[1, 2, 3],
        dict_val={"key": "value"},
    )
    expected = {
        "int_val": 1,
        "str_val": "test",
        "list_val": [1, 2, 3],
        "dict_val": {"key": "value"},
        "none_val": None,
    }

    # 测试基本转换
    assert type_dump_python(model) == expected

    # 测试include参数
    assert type_dump_python(model, include={"int_val", "str_val"}) == {
        "int_val": 1,
        "str_val": "test",
    }

    # 测试exclude参数
    assert type_dump_python(model, exclude={"none_val", "dict_val"}) == {
        "int_val": 1,
        "str_val": "test",
        "list_val": [1, 2, 3],
    }

    # 测试exclude_none参数
    assert "none_val" not in type_dump_python(model, exclude_none=True)


def test_type_dump_json_advanced():
    class ComplexModel(BaseModel):
        int_val: int
        str_val: str
        dict_val: dict[str, Any]

    model = ComplexModel(int_val=1, str_val="test", dict_val={"key": "value"})

    # 基本JSON转换
    json_str = type_dump_json(model)
    assert isinstance(json_str, str)
    assert json.loads(json_str) == {
        "int_val": 1,
        "str_val": "test",
        "dict_val": {"key": "value"},
    }

    # 测试include参数
    json_str = type_dump_json(model, include={"int_val"})
    assert json.loads(json_str) == {"int_val": 1}

    # 测试exclude参数
    json_str = type_dump_json(model, exclude={"dict_val"})
    assert json.loads(json_str) == {"int_val": 1, "str_val": "test"}

    # 测试非模型数据
    json_str = type_dump_json([1, 2, 3])
    assert json.loads(json_str) == [1, 2, 3]

    json_str = type_dump_json({"a": 1, "b": "test"})
    assert json.loads(json_str) == {"a": 1, "b": "test"}
