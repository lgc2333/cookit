from typing import Any, Awaitable, Callable, Literal, Optional, Union
from typing_extensions import TypeAlias

from playwright.async_api import Page

WaitFunction: TypeAlias = Callable[[Page], Awaitable[Any]]
WaitForType: TypeAlias = Union[
    Literal["domcontentloaded", "load", "networkidle"],
    WaitFunction,
    None,
]


async def _wait_for(page: Page, wait_type: WaitForType):
    if callable(wait_type):
        await wait_type(page)
    elif wait_type:
        await page.wait_for_load_state(wait_type)


async def screenshot_selector(page: Page, selector: str, **kwargs) -> bytes:
    elem = await page.query_selector(selector)
    if not elem:
        raise ValueError("Element not found")
    return await elem.screenshot(**kwargs)


async def screenshot_html(
    page: Page,
    html: str,
    selector: Optional[str] = None,
    wait_type: WaitForType = "load",
    **kwargs,
) -> bytes:
    await page.set_content(html)
    await _wait_for(page, wait_type)
    if selector:
        return await screenshot_selector(page, selector, **kwargs)
    return await page.screenshot(**kwargs)
