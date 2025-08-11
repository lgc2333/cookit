import re
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Protocol,
    TypeAlias,
    TypedDict,
    TypeVar,
)
from typing_extensions import Unpack

from playwright.async_api import Page, Request, Route
from yarl import URL

if TYPE_CHECKING:
    from pathlib import Path

PWRouter: TypeAlias = Callable[[Route, Request], Awaitable[Any]]
CKRouterPattern: TypeAlias = str | re.Pattern

T_co = TypeVar("T_co", covariant=True)
TF = TypeVar("TF", bound="CKRouterFunc")


class CKRouterKwArgs(TypedDict):
    route: Route
    request: Request
    info: "CKRouterInfo"
    url: URL
    matched: re.Match[str] | None


class CKRouterFunc(Protocol, Generic[T_co]):
    def __call__(self, **kwds: Unpack[CKRouterKwArgs]) -> Awaitable[T_co]: ...


@dataclass
class CKRouterInfo:
    pattern: CKRouterPattern
    func: CKRouterFunc[Any]
    priority: int


async def apply_router_to_page(page: Page, router: CKRouterInfo):
    async def wrapped(route: Route, request: Request):
        url = URL(request.url)
        matched = (
            re.search(router.pattern, request.url)
            if isinstance(router.pattern, re.Pattern)
            else None
        )
        return await router.func(
            route=route,
            request=request,
            info=router,
            url=url,
            matched=matched,
        )

    await page.route(router.pattern, wrapped)


class RouterGroup:
    def __init__(self, routers: Iterable[CKRouterInfo] | None = None) -> None:
        self.routers: list[CKRouterInfo] = []
        if routers:
            self.routers.extend(routers)

    def register_router(
        self,
        func: CKRouterFunc,
        pattern: CKRouterPattern,
        priority: int = 1,
    ):
        self.routers.append(CKRouterInfo(pattern, func, priority))
        # 低 priority 的 CKRouter 应最先运行，
        # 因为 playwright 后 route 的先运行，所以要反过来排序
        self.routers.sort(key=lambda r: r.priority, reverse=True)

    def router(
        self,
        pattern: CKRouterPattern,
        priority: int = 1,
    ):
        def wrapper(func: TF) -> TF:
            self.register_router(func, pattern, priority)
            return func

        return wrapper

    async def apply(self, page: Page):
        for router in self.routers:
            await apply_router_to_page(page, router)
        return page

    def copy(self) -> "RouterGroup":
        return RouterGroup(self.routers)


def make_real_path_router(path_extractor: CKRouterFunc["Path"]) -> CKRouterFunc:
    async def router(route: Route, matched: re.Match[str] | None, **add_kwds):
        path = await path_extractor(route=route, matched=matched, **add_kwds)
        if (not path.exists()) or (not path.is_file()):
            return await route.fulfill(status=404)
        return await route.fulfill(path=path)

    return router
