from typing import TYPE_CHECKING
from typing_extensions import Unpack

from loguru import logger

if TYPE_CHECKING:
    from ..router import CKRouterFunc, CKRouterKwArgs


def log_router_err(error_code: str | None = None):
    """Create a decorator that logs router errors and aborts the route."""

    def deco(router: "CKRouterFunc") -> "CKRouterFunc":
        async def wrapper(**kwargs: Unpack["CKRouterKwArgs"]):
            try:
                return await router(**kwargs)
            except Exception:
                logger.exception("Error occurred when handling route")
                await kwargs["route"].abort(error_code)

        return wrapper

    return deco
