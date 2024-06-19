from typing import Callable, Dict

from jinja2 import Environment

from ..common import (
    camel_case,
    escape_backticks,
    escape_double_quotes,
    escape_single_quotes,
    full_to_half,
    make_append_func_to_dict_deco,
)

all_filters: Dict[str, Callable] = {}

__append_filter = make_append_func_to_dict_deco(all_filters)


__append_filter(camel_case)
__append_filter(full_to_half)
__append_filter(escape_backticks)
__append_filter(escape_double_quotes)
__append_filter(escape_single_quotes)


@__append_filter
def br(value: str) -> str:
    return value.replace("\n", "<br/>")


def register_all_filters(env: Environment):
    env.filters.update(all_filters)
