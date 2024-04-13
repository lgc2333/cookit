# ruff: noqa: F403

"""Install `cookit[nonebot-alconna]` before import this module."""

from .. import assert_plugin_loaded

assert_plugin_loaded("nonebot_plugin_alconna")
del assert_plugin_loaded

from .receipt import *
from .util import *
