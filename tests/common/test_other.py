# generated by copilot

import asyncio as aio
from typing import List

from cookit.common.other import iter_pagination_func, qor, with_semaphore


def test_qor_with_a_not_none():
    a = 5
    b = 10
    result = qor(a, b)
    assert result == a


def test_qor_with_a_none_and_b_not_callable():
    a = None
    b = 10
    result = qor(a, b)
    assert result == b


def test_qor_with_a_none_and_b_callable():
    a = None
    b = lambda: 10  # noqa: E731
    result = qor(a, b)
    assert result == b()


async def test_with_semaphore():
    ret = "Hello, World!"
    semaphore = aio.Semaphore(1)

    @with_semaphore(semaphore)
    async def async_func():
        return ret

    result = await aio.gather(
        async_func(),
        async_func(),
    )
    assert tuple(result) == (ret, ret)


def get_mock_pagination_func(max_size: int):
    async def mock_pagination_func(page_size: int, offset: int) -> List[int]:
        return list(range(offset, min(offset + page_size, max_size)))

    return mock_pagination_func


async def test_iter_pagination_func():
    func = iter_pagination_func(page_size=3, offset=0)(get_mock_pagination_func(9))
    lst = [x async for x in func()]
    assert lst == [0, 1, 2, 3, 4, 5, 6, 7, 8]


async def test_iter_pagination_func_with_offset():
    func = iter_pagination_func(page_size=3, offset=2)(get_mock_pagination_func(9))
    lst = [x async for x in func()]
    assert lst == [2, 3, 4, 5, 6, 7, 8]


async def test_iter_pagination_func_with_max_size():
    func = iter_pagination_func(page_size=3, offset=0, max_size=5)(
        get_mock_pagination_func(9),
    )
    lst = [x async for x in func()]
    assert lst == [0, 1, 2, 3, 4]