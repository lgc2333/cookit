from typing import Any, Callable, cast

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


def test_append_obj_to_dict_deco():
    from cookit import append_obj_to_dict_deco, make_append_obj_to_dict_deco

    def func1():
        return 1

    def func2():
        return 2

    func_dict1: dict[str, Callable] = {}
    append_obj_to_dict_deco(func_dict1, func1)
    append_obj_to_dict_deco(func_dict1, "func_func2")(func2)
    assert func_dict1 == {"func1": func1, "func_func2": func2}

    func_dict2: dict[str, Callable] = {}
    append_func = make_append_obj_to_dict_deco(func_dict2)
    append_func(func1)
    append_func("func_func2")(func2)
    assert func_dict2 == {"func1": func1, "func_func2": func2}

    class ClassA:
        pass

    class ClassB:
        pass

    class_dict1: dict[str, type] = {}
    append_obj_to_dict_deco(class_dict1, ClassA)
    append_obj_to_dict_deco(class_dict1, "class_class_b")(ClassB)
    assert class_dict1 == {"ClassA": ClassA, "class_class_b": ClassB}

    class_dict2: dict[str, type] = {}
    append_class = make_append_obj_to_dict_deco(class_dict2)
    append_class(ClassA)
    append_class("class_class_b")(ClassB)
    assert class_dict2 == {"ClassA": ClassA, "class_class_b": ClassB}

    obj_dict: dict[str, list[Any]] = {}
    with pytest.raises(TypeError):  # no __name__
        append_obj_to_dict_deco(obj_dict, [])  # type: ignore
