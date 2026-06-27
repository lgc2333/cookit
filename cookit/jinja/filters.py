import re
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Protocol, TypeVar, overload
from urllib.parse import quote

from jinja2.filters import do_mark_safe
from markupsafe import Markup, escape

from ..common import (
    NameDecoCollector,
    camel_case,
    escape_backticks,
    escape_double_quotes,
    escape_single_quotes,
    full_to_half,
)

if TYPE_CHECKING:
    from jinja2 import Environment

    from ..common import HasNameProtocol

    class _HasNameCallable(HasNameProtocol, Protocol):
        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            """Call a named filter function."""
            ...

    TC = TypeVar("TC", bound=_HasNameCallable)

    class _GlobalFilterCollector(NameDecoCollector[Callable]):
        @overload
        def __call__(self, key: str) -> Callable[[TC], TC]:
            """Create a decorator that registers a global filter by name."""
            ...

        @overload
        def __call__(self, key: TC) -> TC:
            """Register a global filter by the callable's __name__."""
            ...

        def __call__(self, key: Any) -> Any:
            """Register a global filter or return a filter decorator."""
            ...

    cookit_global_filter = _GlobalFilterCollector()

else:
    cookit_global_filter = NameDecoCollector[Callable]()


all_filters = cookit_global_filter.data
"""@deprecated: Use `cookit_global_filter.data` instead."""


cookit_global_filter(camel_case)
cookit_global_filter(full_to_half)
cookit_global_filter(escape_backticks)
cookit_global_filter(escape_double_quotes)
cookit_global_filter(escape_single_quotes)


@cookit_global_filter
def br(value: str) -> str:
    """Convert newlines in text to HTML line break tags."""
    return value.replace("\n", "<br/>")


space_re = re.compile(r" {2,}")


@cookit_global_filter
def space(value: str) -> str:
    """Preserve repeated spaces with HTML non-breaking spaces."""
    return space_re.sub(lambda m: f"{'&nbsp;' * (len(m[0]) - 1)} ", value)


@cookit_global_filter
def safe_layout(value: str) -> Markup:
    """Escape text and preserve simple line breaks and repeated spaces as safe HTML."""
    value = str(escape(value))
    value = br(value)
    value = space(value)
    return do_mark_safe(value)


@cookit_global_filter
def url_encode(value: str) -> str:
    """URL-encode text for use in links and query strings."""
    return quote(value)


def register_all_filters(env: "Environment"):
    """Register all cookit global Jinja filters on an environment."""
    env.filters.update(cookit_global_filter.data)
