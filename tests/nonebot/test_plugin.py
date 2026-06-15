import pytest


def test_assert_plugin_loaded_rejects_missing_plugin():
    from cookit.nonebot import assert_plugin_loaded

    with pytest.raises(ImportError, match="You should require plugin `missing_plugin`"):
        assert_plugin_loaded("missing_plugin")
