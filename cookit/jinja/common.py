from typing import TYPE_CHECKING

from ..common import make_append_obj_to_dict_deco

if TYPE_CHECKING:
    from jinja2 import Environment


def make_register_jinja_filter_deco(env: "Environment"):
    return make_append_obj_to_dict_deco(env.filters)
