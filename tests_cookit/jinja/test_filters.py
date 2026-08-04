import jinja2 as jj
from markupsafe import Markup


def test_br():
    from cookit.jinja.filters import br

    assert br("hello\nworld") == "hello<br/>world"
    assert br("hello world") == "hello world"


def test_space_keeps_single_spaces_and_escapes_extra_spaces():
    from cookit.jinja.filters import space

    assert space("a b") == "a b"
    assert space("a  b   c") == "a&nbsp; b&nbsp;&nbsp; c"


def test_safe_layout_escapes_html_then_preserves_layout():
    from cookit.jinja.filters import safe_layout

    result = safe_layout("<b>a  b</b>\nc")

    assert isinstance(result, Markup)
    assert str(result) == "&lt;b&gt;a&nbsp; b&lt;/b&gt;<br/>c"


def test_url_encode():
    from cookit.jinja.filters import url_encode

    assert url_encode("hello world/测试") == "hello%20world/%E6%B5%8B%E8%AF%95"


def test_register_all_filters():
    from cookit.jinja import all_filters, cookit_global_filter, register_all_filters

    env = jj.Environment(autoescape=True)
    register_all_filters(env)
    for k, v in cookit_global_filter.data.items():
        assert env.filters[k] is v
    assert all_filters is cookit_global_filter.data
