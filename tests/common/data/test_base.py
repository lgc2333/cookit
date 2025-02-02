from typing import Callable, cast

import pytest


def test_lazy_get():
    from cookit import LazyGetterType, lazy_get

    a = cast("LazyGetterType[int, []]", 5)
    result = lazy_get(a)
    assert result == a

    b = lambda: 10  # noqa: E731
    result = lazy_get(b)
    assert result == b()

    c = cast("Callable[[int], int]", lambda x: x + 1)  # noqa: E731
    result = lazy_get(c, 1)
    assert result == c(1)


def test_qor_with_a_not_none():
    from cookit import qor

    a = 5
    b = 10
    result = qor(a, b)
    assert result == a


def test_qor_with_a_none_and_b_not_callable():
    from cookit import qor

    a = None
    b = 10
    result = qor(a, b)
    assert result == b


def test_qor_with_a_none_and_b_callable():
    from cookit import qor

    a = None
    b = lambda: 10  # noqa: E731
    result = qor(a, b)
    assert result == b()


def test_chunks():
    from cookit import chunks

    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(chunks(lst, 3)) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    lst2 = [1, 2, 3, 4, 5, 6, 7, 8]
    assert list(chunks(lst2, 3)) == [[1, 2, 3], [4, 5, 6], [7, 8]]


def test_flatten():
    from cookit import flatten

    lst = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert flatten(lst) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_set_default_with_existing_key():
    from cookit import set_default

    target = {"a": 1, "b": 2}
    key = "a"
    default = 10
    result = set_default(target, key, default)
    assert result == target[key]
    assert len(target) == 2


def test_set_default_with_new_key():
    from cookit import set_default

    target = {"a": 1, "b": 2}
    key = "c"
    default = 10
    result = set_default(target, key, default)
    assert result == default
    assert target[key] == default
    assert len(target) == 3


def test_set_default_with_callable_default():
    from cookit import set_default

    target = {"a": 1, "b": 2}
    key = "c"
    default = lambda: 10  # noqa: E731
    result = set_default(target, key, default)
    assert result == default()
    assert target[key] == default()
    assert len(target) == 3


def test_auto_delete():
    from cookit import auto_delete

    # Test case 1: No transformation function provided
    target1 = {"a": 1, "b": 2, "c": None, "d": 0}
    expected_result1 = {"a": 1, "b": 2}
    result1 = auto_delete(target1)
    assert result1 == expected_result1
    assert target1 == expected_result1

    # Test case 2: Transformation function provided
    def transform_func(value: int):
        return value * 2 if value % 2 == 0 else None

    target2 = {"a": 1, "b": 2, "c": 3, "d": 4}
    expected_result2 = {"b": 2, "d": 4}
    expected_result2_transformed = {"b": 4, "d": 8}
    result2 = auto_delete(target2, transform=transform_func)
    assert result2 == expected_result2_transformed
    assert target2 == expected_result2

    # Test case 3: Empty target dictionary
    target3 = {}
    expected_result3 = {}
    result3 = auto_delete(target3)
    assert result3 == expected_result3
    assert target3 == expected_result3


def test_deco_collector():
    from cookit import DecoCollector

    collector = DecoCollector[str, int]()
    collector("test1")(1)
    assert collector.data == {"test1": 1}
    collector("test2")(2)
    assert collector.data == {"test1": 1, "test2": 2}
    with pytest.raises(ValueError, match="Object with key 'test1' already exists"):
        collector("test1")(114514)

    collector2_data: dict[str, int] = {}
    collector2 = DecoCollector(collector2_data, allow_overwrite=True)
    collector2("test2_1")(1)
    assert collector2.data == {"test2_1": 1}
    assert collector2.data is collector2_data
    collector2("test2_1")(114514)
    assert collector2.data == {"test2_1": 114514}


def test_type_deco_collector():
    from cookit import TypeDecoCollector

    class BaseCls:
        pass

    class Cls1(BaseCls):
        pass

    class Cls2(BaseCls):
        pass

    collector = TypeDecoCollector[BaseCls, int]()
    collector(Cls1)(1)
    assert collector.data == {Cls1: 1}
    collector(Cls2)(2)
    assert collector.data == {Cls1: 1, Cls2: 2}
    with pytest.raises(
        ValueError,
        match="Object with key '<class '.+Cls1'>' already exists",
    ):
        collector(Cls1)(114514)


def test_name_deco_collector():
    from cookit import NameDecoCollector

    class Cls1:
        pass

    class Cls2:
        pass

    collector = NameDecoCollector[type]()
    collector(Cls1)
    assert collector.data == {"Cls1": Cls1}
    with pytest.raises(ValueError, match="Object with key 'Cls1' already exists"):
        collector(Cls1)
    collector("ClsABC")(Cls2)
    assert collector.data == {"Cls1": Cls1, "ClsABC": Cls2}
    with pytest.raises(ValueError, match="Object with key 'Cls1' already exists"):
        collector("Cls1")(Cls2)
