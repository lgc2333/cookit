from typing import TYPE_CHECKING

import pytest
from playwright.async_api import Error as PWError

from ...loguru.utils import LoggingContext

if TYPE_CHECKING:
    from playwright.async_api import Page


pytestmark = pytest.mark.asyncio(loop_scope="session")

ROUTE_BASE_URL = "https://cookit.route"


async def test_log_router_err(page: "Page"):
    from cookit.pw import RouterGroup
    from cookit.pw.loguru import log_router_err

    router_group = RouterGroup()

    @router_group.router(f"{ROUTE_BASE_URL}/**/*")
    @log_router_err()
    async def _(**_):
        raise RuntimeError

    await router_group.apply(page)
    with LoggingContext() as ctx:
        with pytest.raises(PWError):
            await page.goto(f"{ROUTE_BASE_URL}/")
        ctx.should_log(
            exception=RuntimeError,
            message="Error occurred when handling route",
        )
