from pathlib import Path

from ..utils import expect_exc, mark_test
from .utils import get_page

html_text = (Path(__file__).parent / "test.html").read_text("u8")


@mark_test
async def test_screenshot_selector():
    from cookit.pw import screenshot_selector

    async with await get_page() as page:
        await page.set_content(html_text)
        await screenshot_selector(page, "h1")
        with expect_exc(ValueError):
            await screenshot_selector(page, "h5")


@mark_test
async def test_screenshot_html():
    from cookit.pw import screenshot_html

    async with await get_page() as page:
        await screenshot_html(page, html_text)

    async with await get_page() as page:
        await screenshot_html(page, html_text, "h1")

    async with await get_page() as page:
        with expect_exc(ValueError):
            await screenshot_html(page, html_text, "h5")
