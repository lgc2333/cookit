import asyncio as aio


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
