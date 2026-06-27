from collections.abc import Awaitable, Callable
from typing import Any, Literal, TypeAlias

from playwright.async_api import Page

WaitFunction: TypeAlias = Callable[[Page], Awaitable[Any]]
WaitForType: TypeAlias = (
    Literal["domcontentloaded", "load", "networkidle"] | WaitFunction | None
)


async def _wait_for(page: Page, wait_type: WaitForType):
    """Wait for a Playwright page load state or custom wait function."""
    if callable(wait_type):
        await wait_type(page)
    elif wait_type:
        await page.wait_for_load_state(wait_type)


async def screenshot_selector(page: Page, selector: str, **kwargs) -> bytes:
    """Capture a screenshot of a selected element."""
    elem = await page.query_selector(selector)
    if not elem:
        raise ValueError("Element not found")
    return await elem.screenshot(**kwargs)


async def screenshot_html(
    page: Page,
    html: str,
    selector: str | None = None,
    wait_type: WaitForType = "load",
    **kwargs,
) -> bytes:
    """Render HTML in a page and capture either the page or a selector."""
    await page.set_content(html)
    await _wait_for(page, wait_type)
    if selector:
        return await screenshot_selector(page, selector, **kwargs)
    return await page.screenshot(**kwargs)
