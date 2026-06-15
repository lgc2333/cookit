import pytest

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


def test_append_obj_to_dict_deco_registers_object_by_name():
    from cookit.common.deprecated import append_obj_to_dict_deco

    registry = {}

    class Plugin:
        pass

    result = append_obj_to_dict_deco(registry, Plugin)

    assert result is Plugin
    assert registry == {"Plugin": Plugin}


def test_append_obj_to_dict_deco_registers_with_explicit_name():
    from cookit.common.deprecated import append_obj_to_dict_deco

    registry = {}

    @append_obj_to_dict_deco(registry, "custom")
    def handler():
        return "ok"

    assert registry == {"custom": handler}
    assert handler() == "ok"


def test_append_obj_to_dict_deco_rejects_duplicate_without_overwrite():
    from cookit.common.deprecated import append_obj_to_dict_deco

    registry = {"name": object()}

    with pytest.raises(ValueError, match="Object with name 'name' already exists"):
        append_obj_to_dict_deco(registry, "name", allow_overwrite=False)(object())


def test_append_obj_to_dict_deco_rejects_unnamed_object():
    from cookit.common.deprecated import append_obj_to_dict_deco

    with pytest.raises(TypeError, match="func_or_name must be str"):
        append_obj_to_dict_deco({}, object())


def test_make_append_obj_to_dict_deco_preserves_options():
    from cookit.common.deprecated import make_append_obj_to_dict_deco

    registry = {"handler": object()}
    deco = make_append_obj_to_dict_deco(registry, allow_overwrite=False)

    with pytest.raises(ValueError, match="Object with name 'handler' already exists"):

        @deco("handler")
        def handler():
            return None


def test_append_func_to_dict_deco_delegates_to_object_decorator():
    from cookit.common.deprecated import append_func_to_dict_deco

    registry = {}

    @append_func_to_dict_deco(registry, "handler")
    def handler():
        return "ok"

    assert registry == {"handler": handler}


def test_make_append_func_to_dict_deco_creates_function_decorator():
    from cookit.common.deprecated import make_append_func_to_dict_deco

    registry = {}
    deco = make_append_func_to_dict_deco(registry)

    @deco("handler")
    def handler():
        return "ok"

    assert registry == {"handler": handler}
