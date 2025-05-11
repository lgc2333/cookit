from typing import Callable

import pytest


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


def test_deco_list_collector():
    from cookit import DecoListCollector

    # 测试基本功能 - 使用正确的类型注解
    collector = DecoListCollector[Callable[[], int]]()

    @collector
    def func1() -> int:
        return 1

    @collector
    def func2() -> int:
        return 2

    assert collector.data == [func1, func2]
    assert func1() == 1  # 确保装饰器不影响原函数功能
    assert func2() == 2

    # 测试初始化时传入列表
    initial_list: list[Callable[[], int]] = [lambda: 3]
    collector2 = DecoListCollector[Callable[[], int]](initial_list)

    @collector2
    def func3() -> int:
        return 4

    assert collector2.data == [initial_list[0], func3]
    assert collector2.data is initial_list  # 确保使用的是同一个列表对象
    assert collector2.data[0]() == 3
    assert collector2.data[1]() == 4
