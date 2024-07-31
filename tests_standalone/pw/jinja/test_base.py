from pathlib import Path

import jinja2

from ...utils import expect_exc, mark_test
from ..utils import get_page


@mark_test
async def test_template_renderer():
    from cookit.pw.jinja import make_template_renderer

    template_text = (Path(__file__).parent / "test.html.jinja").read_text("u8")
    template = jinja2.Template(template_text, autoescape=True, enable_async=True)
    renderer = await make_template_renderer(template, title_tag="h1")

    async with await get_page() as page:
        await renderer(page)

    async with await get_page() as page:
        await renderer(page, "h1")

    async with await get_page() as page:
        with expect_exc(ValueError):
            await renderer(page, "h5")
