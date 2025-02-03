async def test_async_nullcontext():
    from cookit.common.compat import nullcontext

    async with nullcontext() as value:
        assert value is None

    async with nullcontext(42) as value:
        assert value == 42
