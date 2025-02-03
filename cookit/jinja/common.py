from typing import TYPE_CHECKING, Callable

from ..common import NameDecoCollector

if TYPE_CHECKING:
    from jinja2 import Environment


def make_register_jinja_filter_deco(env: "Environment"):
    return NameDecoCollector[Callable](env.filters)
