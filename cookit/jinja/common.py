from jinja2 import Environment

from ..common import make_append_func_to_dict_deco


def make_register_jinja_filter_deco(env: Environment):
    return make_append_func_to_dict_deco(env.filters)
