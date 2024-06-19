import jinja2 as jj


def test_br():
    from cookit.jinja.filters import br

    assert br("hello\nworld") == "hello<br/>world"
    assert br("hello world") == "hello world"


def test_register_all_filters():
    from cookit.jinja import all_filters, register_all_filters

    env = jj.Environment(autoescape=True)
    register_all_filters(env)
    for k, v in all_filters.items():
        assert env.filters[k] is v
