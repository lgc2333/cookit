"""Install `cookit[nonebot-alconna]` before import this module."""

# region assert required plugin loaded
from .. import assert_plugin_loaded

assert_plugin_loaded("nonebot_plugin_alconna")
del assert_plugin_loaded
# endregion

# ruff: noqa: E402
from .common import (
    extract_reply_msg as extract_reply_msg,
)
from .receipt import (
    RecallContext as RecallContext,
)
