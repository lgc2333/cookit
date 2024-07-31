"""Install `cookit[playwright]` before import this module."""

from .router import (
    CKRouterFunc as CKRouterFunc,
    CKRouterInfo as CKRouterInfo,
    CKRouterKwArgs as CKRouterKwArgs,
    CKRouterPattern as CKRouterPattern,
    PWRouter as PWRouter,
    RouterGroup as RouterGroup,
    apply_router_to_page as apply_router_to_page,
    make_real_path_router as make_real_path_router,
)
from .screenshot import (
    WaitForType as WaitForType,
    WaitFunction as WaitFunction,
    screenshot_html as screenshot_html,
    screenshot_selector as screenshot_selector,
)
