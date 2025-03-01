"""Install `cookit[nonebot-localstore]` before import this module."""

# region assert required plugin loaded
from .. import assert_plugin_loaded

assert_plugin_loaded("nonebot_plugin_localstore")
del assert_plugin_loaded
# endregion

# ruff: noqa: E402
from .base import (
    LOCALSTORE_DEFAULT_PATH_WARNING_MSG as LOCALSTORE_DEFAULT_PATH_WARNING_MSG,
    ensure_localstore_path_config as ensure_localstore_path_config,
)
