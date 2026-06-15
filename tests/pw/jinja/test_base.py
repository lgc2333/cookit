from pathlib import Path
from typing import TYPE_CHECKING

import jinja2
import pytest

if TYPE_CHECKING:
    from playwright.async_api import Page


pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_template_renderer(page: "Page"):
    from cookit.pw.jinja import make_template_renderer

    template_text = (Path(__file__).parent / "test.html.jinja").read_text("u8")
    template = jinja2.Template(template_text, autoescape=True, enable_async=True)
    renderer = await make_template_renderer(template, title_tag="h1")

    await renderer(page)
    await renderer(page, "h1")
    with pytest.raises(ValueError, match="Element not found"):
        await renderer(page, "h5")
