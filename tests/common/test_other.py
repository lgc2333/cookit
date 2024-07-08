import asyncio as aio

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

    ret = "Hello, World!"
    counter = 0

    @queued
    async def async_func():
        nonlocal counter
        await aio.sleep(0)
        counter += 1
        return f"{ret}{counter}"

    result = await aio.gather(
        async_func(),
        async_func(),
        async_func(),
        async_func(),
        async_func(),
    )
    assert tuple(result) == (f"{ret}1", f"{ret}2", f"{ret}3", f"{ret}4", f"{ret}5")


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
