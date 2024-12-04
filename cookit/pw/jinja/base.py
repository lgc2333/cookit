from typing import TYPE_CHECKING, Optional

from ..screenshot import screenshot_html

if TYPE_CHECKING:
    from jinja2 import Template
    from playwright.async_api import Page


async def make_template_renderer(template: "Template", **template_kwargs):
    html = await template.render_async(**template_kwargs)

    async def render(page: "Page", selector: Optional[str] = None, **screenshot_kwargs):
        return await screenshot_html(page, html, selector, **screenshot_kwargs)

    return render
