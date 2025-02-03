import jinja2 as jj


def test_br():
    from cookit.jinja.filters import br

    assert br("hello\nworld") == "hello<br/>world"
    assert br("hello world") == "hello world"


def test_register_all_filters():
    from cookit.jinja import cookit_global_filter, register_all_filters

    env = jj.Environment(autoescape=True)
    register_all_filters(env)
    for k, v in cookit_global_filter.data.items():
        assert env.filters[k] is v
