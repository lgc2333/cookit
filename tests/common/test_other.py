import asyncio as aio
from pathlib import Path
from typing import List

import pytest


async def test_with_semaphore():
    from cookit import with_semaphore

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


async def test_queued():
    from cookit import queued

    counter = 0
    count_list: List[int] = []

    @queued
    async def async_func():
        nonlocal counter
        counter += 1
        await aio.sleep(0)
        count_list.append(counter)

    await aio.gather(
        async_func(),
        async_func(),
        async_func(),
        async_func(),
        async_func(),
    )
    assert count_list == [1, 2, 3, 4, 5]


async def test_race():
    from cookit import race

    async def f1():
        await aio.sleep(1)
        return 1

    async def f2():
        await aio.sleep(2)
        return 2

    async def fe():
        raise Exception

    assert await race(f1(), f2()) == 1
    with pytest.raises(Exception):  # noqa: B017, PT011
        await race(f1(), f2(), fe())


def test_auto_import():
    from cookit import auto_import

    from .auto_import.base import get_counter

    for m in auto_import(
        Path(__file__).parent / "auto_import",
        f"{__package__}.auto_import",
    ):
        if hasattr(m, "main"):
            m.main()
    assert get_counter() == 2

    for m in auto_import(
        Path(__file__).parent / "auto_import",
        f"{__package__}.auto_import",
        lambda _: True,
    ):
        if hasattr(m, "main"):
            m.main()
    assert get_counter() == 5
