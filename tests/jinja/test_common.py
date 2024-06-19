from typing import Any

import jinja2 as jj


def test_make_register_jinja_filter_deco():
    from cookit.jinja import make_register_jinja_filter_deco

    env = jj.Environment(autoescape=True)
    register_filter = make_register_jinja_filter_deco(env)

    def test_filter(val: Any) -> str:
        return f"test, {val}"

    register_filter(test_filter)
    register_filter("test_test_filter")(test_filter)

    assert env.filters["test_filter"] is test_filter
    assert env.filters["test_test_filter"] is test_filter
