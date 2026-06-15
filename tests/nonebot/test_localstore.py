from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from nonebug import App


def make_localstore_config(**overrides):
    data = {
        "localstore_use_cwd": False,
        "localstore_cache_dir": None,
        "localstore_config_dir": None,
        "localstore_data_dir": None,
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def test_localstore_module_imports_after_required_plugin(app: "App"):  # noqa: ARG001
    from nonebot import require

    require("nonebot_plugin_localstore")

    from cookit.nonebot import localstore

    assert localstore.LOCALSTORE_DEFAULT_PATH_WARNING_MSG
    assert callable(localstore.ensure_localstore_path_config)


def test_ensure_localstore_path_config_accepts_cwd_config(
    app: "App",  # noqa: ARG001
    monkeypatch: pytest.MonkeyPatch,
):
    from nonebot import require

    require("nonebot_plugin_localstore")

    from cookit.nonebot.localstore import base

    monkeypatch.setattr(
        base,
        "localstore_config",
        make_localstore_config(localstore_use_cwd=True),
    )

    base.ensure_localstore_path_config()


def test_ensure_localstore_path_config_accepts_explicit_dirs(
    app: "App",  # noqa: ARG001
    monkeypatch: pytest.MonkeyPatch,
):
    from nonebot import require

    require("nonebot_plugin_localstore")

    from cookit.nonebot.localstore import base

    for field in (
        "localstore_cache_dir",
        "localstore_config_dir",
        "localstore_data_dir",
    ):
        monkeypatch.setattr(
            base,
            "localstore_config",
            make_localstore_config(**{field: object()}),
        )
        base.ensure_localstore_path_config()


def test_ensure_localstore_path_config_accepts_explicit_opt_in(
    app: "App",  # noqa: ARG001
    monkeypatch: pytest.MonkeyPatch,
):
    from nonebot import require

    require("nonebot_plugin_localstore")

    from cookit.nonebot.localstore import base

    monkeypatch.setattr(base, "localstore_config", make_localstore_config())
    monkeypatch.setattr(
        base,
        "get_plugin_config",
        lambda _model: SimpleNamespace(sure=True),
    )

    base.ensure_localstore_path_config()


def test_ensure_localstore_path_config_rejects_default_paths(
    app: "App",  # noqa: ARG001
    monkeypatch: pytest.MonkeyPatch,
):
    from nonebot import require

    require("nonebot_plugin_localstore")

    from cookit.nonebot.localstore import base

    monkeypatch.setattr(base, "localstore_config", make_localstore_config())
    monkeypatch.setattr(
        base,
        "get_plugin_config",
        lambda _model: SimpleNamespace(sure=False),
    )

    with pytest.raises(RuntimeError, match="REFUSE TO LOAD"):
        base.ensure_localstore_path_config()
