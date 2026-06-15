def get_mock_pagination_func(max_size: int):
    async def mock_pagination_func(page_size: int, offset: int) -> list[int]:
        return list(range(offset, min(offset + page_size, max_size)))

    return mock_pagination_func


async def test_iter_pagination_func():
    from cookit import iter_pagination_func

    func = iter_pagination_func(page_size=3, offset=0)(get_mock_pagination_func(9))
    lst = [x async for x in func()]
    assert lst == [0, 1, 2, 3, 4, 5, 6, 7, 8]


async def test_iter_pagination_func_with_offset():
    from cookit import iter_pagination_func

    func = iter_pagination_func(page_size=3, offset=2)(get_mock_pagination_func(9))
    lst = [x async for x in func()]
    assert lst == [2, 3, 4, 5, 6, 7, 8]


async def test_iter_pagination_func_with_max_size():
    from cookit import iter_pagination_func

    func = iter_pagination_func(page_size=3, offset=0, max_size=5)(
        get_mock_pagination_func(9),
    )
    lst = [x async for x in func()]
    assert lst == [0, 1, 2, 3, 4]


async def test_iter_pagination_func_stops_when_page_is_empty():
    from cookit import iter_pagination_func

    calls: list[tuple[int, int]] = []

    async def mock_pagination_func(page_size: int, offset: int) -> list[int]:
        calls.append((page_size, offset))
        return []

    func = iter_pagination_func(page_size=3, offset=6)(mock_pagination_func)

    assert [x async for x in func()] == []
    assert calls == [(3, 6)]


async def test_iter_pagination_func_honors_delay_between_non_final_pages():
    from cookit import iter_pagination_func

    calls: list[tuple[int, int]] = []

    async def mock_pagination_func(page_size: int, offset: int) -> list[int]:
        calls.append((page_size, offset))
        if offset >= 2:
            return []
        return [offset]

    func = iter_pagination_func(page_size=1, delay=0.001)(mock_pagination_func)

    assert [x async for x in func()] == [0, 1]
    assert calls == [(1, 0), (1, 1), (1, 2)]
