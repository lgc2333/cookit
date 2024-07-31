from typing import Optional

from playwright.async_api import Page


async def screenshot_selector(page: Page, selector: str, **kwargs) -> bytes:
    elem = await page.query_selector(selector)
    if not elem:
        raise ValueError("Element not found")
    return await elem.screenshot(**kwargs)


async def screenshot_html(
    page: Page,
    html: str,
    selector: Optional[str] = None,
    **kwargs,
) -> bytes:
    await page.set_content(html)
    if selector:
        return await screenshot_selector(page, selector, **kwargs)
    return await page.screenshot(**kwargs)
