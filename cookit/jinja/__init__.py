"""Install `cookit[jinja]` before import this module."""

from . import filters as filters
from .common import (
    make_register_jinja_filter_deco as make_register_jinja_filter_deco,
)
from .filters import (
    all_filters as all_filters,
    cookit_global_filter as cookit_global_filter,
    register_all_filters as register_all_filters,
)
