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
        def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    TC = TypeVar("TC", bound=_HasNameCallable)

    class _GlobalFilterCollector(NameDecoCollector[Callable]):
        @overload
        def __call__(self, key: str) -> Callable[[TC], TC]: ...
        @overload
        def __call__(self, key: TC) -> TC: ...
        def __call__(self, key: Any) -> Any: ...

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
    return value.replace("\n", "<br/>")


space_re = re.compile(r" {2,}")


@cookit_global_filter
def space(value: str) -> str:
    return space_re.sub(lambda m: f"{'&nbsp;' * (len(m[0]) - 1)} ", value)


@cookit_global_filter
def safe_layout(value: str) -> Markup:
    value = str(escape(value))
    value = br(value)
    value = space(value)
    return do_mark_safe(value)


@cookit_global_filter
def url_encode(value: str) -> str:
    return quote(value)


def register_all_filters(env: "Environment"):
    env.filters.update(cookit_global_filter.data)
