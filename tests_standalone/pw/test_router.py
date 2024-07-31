import re
from pathlib import Path
from typing import Optional, cast

from playwright.async_api import Route
from yarl import URL

from ..utils import mark_test
from .utils import get_page

ROUTE_BASE_URL = "https://cookit.route"


@mark_test
async def test_router_group_route():
    from cookit.pw import RouterGroup

    router_group = RouterGroup()

    body_root = "root"

    @router_group.router(f"{ROUTE_BASE_URL}/")
    async def _(route: Route, **_):
        await route.fulfill(body=body_root)

    body_test = "test"

    @router_group.router(f"{ROUTE_BASE_URL}/test/**/*")
    @router_group.router(f"{ROUTE_BASE_URL}/test")
    async def _(route: Route, **_):
        await route.fulfill(body=body_test)

    body_test2_re = "test2_re"

    last_matched = cast(Optional[re.Match[str]], None)

    @router_group.router(re.compile(rf"{ROUTE_BASE_URL}/test2(/.*)?"))
    async def _(route: Route, matched: Optional[re.Match[str]], **_):
        nonlocal last_matched
        last_matched = matched
        await route.fulfill(body=body_test2_re)

    async with await get_page() as page:
        await router_group.apply(page)

        resp = await page.goto(f"{ROUTE_BASE_URL}/")
        assert resp
        assert (await resp.body()).decode() == body_root

        resp = await page.goto(f"{ROUTE_BASE_URL}/test")
        assert resp
        assert (await resp.body()).decode() == body_test

        resp = await page.goto(f"{ROUTE_BASE_URL}/test/test/test")
        assert resp
        assert (await resp.body()).decode() == body_test

        resp = await page.goto(f"{ROUTE_BASE_URL}/test2")
        assert resp
        assert (await resp.body()).decode() == body_test2_re
        assert last_matched
        assert not last_matched[1]

        resp = await page.goto(f"{ROUTE_BASE_URL}/test2/test")
        assert resp
        assert (await resp.body()).decode() == body_test2_re
        assert last_matched
        assert last_matched[1] == "/test"


@mark_test
async def test_real_path_router():
    from cookit.pw import RouterGroup, make_real_path_router

    router_group = RouterGroup()

    base_path = Path(__file__).parent

    @router_group.router(f"{ROUTE_BASE_URL}/**/*")
    @make_real_path_router
    async def _(url: URL, **_):
        return base_path.joinpath(url.path[1:])

    async with await get_page() as page:
        await router_group.apply(page)

        resp = await page.goto(f"{ROUTE_BASE_URL}/test.html")
        assert resp
        assert (await resp.body()) == (base_path / "test.html").read_bytes()

        resp = await page.goto(f"{ROUTE_BASE_URL}/unknown_file.html")
        assert resp
        assert resp.status == 404


@mark_test
async def test_router_group_copy():
    from cookit.pw import RouterGroup

    router_group = RouterGroup()

    @router_group.router(f"{ROUTE_BASE_URL}/test")
    async def _(route: Route, **_):
        await route.fulfill(body=b"")

    router_group2 = router_group.copy()

    @router_group2.router(f"{ROUTE_BASE_URL}/test2")
    async def _(route: Route, **_):
        await route.fulfill(body=b"")

    assert router_group.routers is not router_group2.routers
    assert len(router_group.routers) == 1
    assert len(router_group2.routers) == 2
