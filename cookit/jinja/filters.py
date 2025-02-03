from typing import TYPE_CHECKING, Callable

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


def register_all_filters(env: "Environment"):
    env.filters.update(cookit_global_filter.data)
