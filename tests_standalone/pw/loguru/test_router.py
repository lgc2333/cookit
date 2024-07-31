from playwright.async_api import Error as PWError
from tests.loguru.utils import LoggingContext

from ...utils import expect_exc, mark_test
from ..utils import get_page

ROUTE_BASE_URL = "https://cookit.route"


@mark_test
async def test_log_router_err():
    from cookit.pw import RouterGroup
    from cookit.pw.loguru import log_router_err

    router_group = RouterGroup()

    @router_group.router(f"{ROUTE_BASE_URL}/**/*")
    @log_router_err()
    async def _(**_):
        raise RuntimeError

    async with await get_page() as page:
        await router_group.apply(page)
        with LoggingContext() as ctx:
            with expect_exc(PWError):
                await page.goto(f"{ROUTE_BASE_URL}/")
            ctx.should_log(
                exception=RuntimeError,
                message="Error occurred when handling route",
            )
