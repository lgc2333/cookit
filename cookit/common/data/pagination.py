import asyncio
from functools import wraps
from typing import (
    AsyncIterable,
    Callable,
    Generic,
    List,
    Optional,
    Protocol,
    TypedDict,
    TypeVar,
)
from typing_extensions import NotRequired, Unpack

T = TypeVar("T")


class PaginationCallable(Protocol, Generic[T]):
    async def __call__(self, page_size: int, offset: int) -> Optional[List[T]]: ...


class IterPFKwargs(TypedDict):
    """分页查询相关参数"""

    page_size: NotRequired[int]
    """单次查询的数量，默认为 `100`"""
    offset: NotRequired[int]
    """查询的初始偏移量，默认为 `0`"""
    delay: NotRequired[float]
    """每次查询后的延迟时间，单位秒，默认为 `0`"""
    max_size: NotRequired[int]
    """最大结果数，返回的结果数永远不会超过这个值，默认为 `0`，即不限制"""


def iter_pagination_func(**kwargs: Unpack[IterPFKwargs]):
    page_size = kwargs.get("page_size", 100)
    offset = kwargs.get("offset", 0)
    delay = kwargs.get("delay", 0.0)
    max_size = kwargs.get("max_size", 0)
    has_max_size = max_size > 0

    def decorator(func: PaginationCallable[T]) -> Callable[[], AsyncIterable[T]]:
        @wraps(func)
        async def wrapper():
            now_offset = offset
            while True:
                # 如果声明了最大结果数，
                # 那么确保 本次查询的数量 不会超过 剩余的最大结果数
                now_page_size = (
                    min(page_size, max_size - now_offset) if has_max_size else page_size
                )

                resp = await func(now_page_size, now_offset)
                if not resp:
                    break  # 无结果结束迭代

                for x in resp:
                    yield x

                now_offset += page_size
                if max_size > 0 and now_offset >= max_size:
                    break

                if delay:
                    await asyncio.sleep(delay)

        return wrapper

    return decorator
