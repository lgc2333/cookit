from typing import Optional
from typing_extensions import Unpack

from loguru import logger

from ..router import CKRouterFunc, CKRouterKwArgs


def log_router_err(error_code: Optional[str] = None):
    def deco(router: CKRouterFunc) -> CKRouterFunc:
        async def wrapper(**kwargs: Unpack[CKRouterKwArgs]):
            try:
                return await router(**kwargs)
            except Exception:
                logger.exception("Error occurred when handling route")
                await kwargs["route"].abort(error_code)

        return wrapper

    return deco
