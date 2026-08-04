from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from playwright.async_api import Page


pytestmark = pytest.mark.asyncio(loop_scope="session")

html_text = (Path(__file__).parent / "test.html").read_text("u8")


async def test_screenshot_selector(page: "Page"):
    from cookit.pw import screenshot_selector

    await page.set_content(html_text)
    await screenshot_selector(page, "h1")
    with pytest.raises(ValueError, match="Element not found"):
        await screenshot_selector(page, "h5")


async def test_screenshot_html(page: "Page"):
    from cookit.pw import screenshot_html

    await screenshot_html(page, html_text)
    await screenshot_html(page, html_text, "h1")
    with pytest.raises(ValueError, match="Element not found"):
        await screenshot_html(page, html_text, "h5")


async def test_screenshot_html_accepts_custom_wait_function(page: "Page"):
    from cookit.pw import screenshot_html

    waited = False

    async def wait_for_title(p: "Page"):
        nonlocal waited
        waited = True
        await p.wait_for_selector("h1")

    await screenshot_html(page, html_text, wait_type=wait_for_title)

    assert waited
