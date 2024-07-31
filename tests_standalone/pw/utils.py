from typing import Optional

from playwright.async_api import Browser, Playwright, async_playwright

from tests_standalone.utils import mark_before_exit

pw: Optional[Playwright] = None
browser: Optional[Browser] = None


async def get_playwright():
    global pw
    if not pw:
        pw = await async_playwright().start()
    return pw


async def get_browser():
    global browser
    if not browser:
        browser = await (await get_playwright()).chromium.launch()
    return browser


async def get_page():
    return await (await get_browser()).new_page()


@mark_before_exit
async def _():
    if browser:
        await browser.close()
    if pw:
        await pw.stop()
