import asyncio
from typing import Any

import pytest
from cookit.common.signal import Signal, default_exc_handler, safe_exc_handler


async def _slot(n: int) -> int:
    """测试用的简单槽函数，返回输入值"""
    await asyncio.sleep(0.01)  # 模拟异步操作
    return n


async def _slot_with_args(n: int, m: int) -> int:
    """测试用的带多参数的槽函数，返回参数和"""
    await asyncio.sleep(0.01)  # 模拟异步操作
    return n + m


async def _failing_slot(_: int) -> int:
    """测试用的抛出异常的槽函数"""
    await asyncio.sleep(0.01)  # 模拟异步操作
    raise ValueError("测试异常")


async def test_connect():
    """测试连接槽函数到信号"""
    signal = Signal[[int], int, Any]()

    # 连接槽函数
    signal.connect(_slot)
    assert len(signal.slots) == 1
    assert signal.slots[0] == _slot

    # 再次连接另一个槽函数
    signal.connect(_slot)
    assert len(signal.slots) == 2


async def test_run():
    """测试单个槽函数的执行"""
    signal = Signal[[int], int, Any]()

    # 测试正常执行
    result = await signal.run(_slot, 5)
    assert result == 5

    # 测试多参数执行
    signal_with_args = Signal[[int, int], int, Any]()
    result = await signal_with_args.run(_slot_with_args, 3, 4)
    assert result == 7


async def test_sequential():
    """测试顺序执行所有槽函数"""
    signal = Signal[[int], int, Any]()

    # 连接多个槽函数
    signal.connect(_slot)
    signal.connect(lambda n: _slot(n * 2))
    signal.connect(lambda n: _slot(n * 3))

    # 顺序执行
    results = await signal.sequential(5)
    assert results == [5, 10, 15]


async def test_gather():
    """测试并行执行所有槽函数"""
    signal = Signal[[int], int, Any]()

    # 连接多个槽函数
    signal.connect(_slot)
    signal.connect(lambda n: _slot(n * 2))
    signal.connect(lambda n: _slot(n * 3))

    # 并行执行
    results = await signal.gather(5)
    # 由于是并行执行，结果顺序应该与槽函数添加顺序一致
    assert sorted(results) == [5, 10, 15]


async def test_task_sequential():
    """测试作为任务顺序执行所有槽函数"""
    signal = Signal[[int], int, Any]()

    # 连接多个槽函数
    signal.connect(_slot)
    signal.connect(lambda n: _slot(n * 2))

    # 创建任务并等待结果
    task = signal.task_sequential(5)
    assert isinstance(task, asyncio.Task)
    results = await task
    assert results == [5, 10]


async def test_task_gather():
    """测试作为任务并行执行所有槽函数"""
    signal = Signal[[int], int, Any]()

    # 连接多个槽函数
    signal.connect(_slot)
    signal.connect(lambda n: _slot(n * 2))

    # 创建任务并等待结果
    task = signal.task_gather(5)
    assert isinstance(task, asyncio.Task)
    results = await task
    assert sorted(results) == [5, 10]


async def test_default_exc_handler():
    """测试默认异常处理器会传播异常"""
    signal = Signal[[int], int, Any](exc_handler=default_exc_handler)
    signal.connect(_failing_slot)

    # 默认异常处理器会重新抛出异常
    with pytest.raises(ValueError, match="测试异常"):
        await signal.sequential(5)


async def test_safe_exc_handler():
    """测试安全异常处理器会返回异常对象而不是传播"""
    signal = Signal[[int], int, Exception](exc_handler=safe_exc_handler)
    signal.connect(_slot)  # 正常槽函数
    signal.connect(_failing_slot)  # 会抛出异常的槽函数

    # 安全异常处理器会返回异常对象
    results = await signal.sequential(5)
    assert len(results) == 2
    assert results[0] == 5  # 第一个正常返回
    assert isinstance(results[1], ValueError)  # 第二个返回异常对象
    assert str(results[1]) == "测试异常"


async def test_custom_exc_handler():
    """测试自定义异常处理器"""

    async def custom_handler(_sig: Signal, exc: Exception) -> str:
        return f"错误: {exc!s}"

    signal = Signal[[int], int, str](exc_handler=custom_handler)
    signal.connect(_failing_slot)

    # 自定义异常处理器会返回自定义的错误消息
    results = await signal.sequential(5)
    assert results == ["错误: 测试异常"]


async def test_mixed_results():
    """测试混合的结果类型 (正常返回值 + 异常)"""
    signal = Signal[[int], int, Exception](exc_handler=safe_exc_handler)

    # 添加一些正常和异常的槽函数
    signal.connect(_slot)
    signal.connect(_failing_slot)
    signal.connect(lambda n: _slot(n * 2))

    # 测试顺序执行
    seq_results = await signal.sequential(5)
    assert len(seq_results) == 3
    assert seq_results[0] == 5
    assert isinstance(seq_results[1], ValueError)
    assert seq_results[2] == 10

    # 测试并行执行
    gather_results = await signal.gather(5)
    assert len(gather_results) == 3

    # 验证结果类型和值（顺序可能不确定，但应该有两个整数和一个异常）
    integers = [r for r in gather_results if isinstance(r, int)]
    exceptions = [r for r in gather_results if isinstance(r, Exception)]
    assert sorted(integers) == [5, 10]
    assert len(exceptions) == 1
    assert isinstance(exceptions[0], ValueError)
