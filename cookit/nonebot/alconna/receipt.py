import asyncio as aio
import random
from typing import TYPE_CHECKING, Optional, Union

from nonebot import logger
from nonebot_plugin_alconna.uniseg import (  # noqa: E402
    Receipt,
    Reply,
    Target,
    UniMessage,
)

if TYPE_CHECKING:
    from nonebot.adapters import Bot as BaseBot, Event as BaseEvent


class RecallContext:
    def __init__(
        self,
        delay: Union[float, tuple[float, float], None] = None,
        wait: bool = False,
    ) -> None:
        self.delay = delay
        self.wait = wait
        self.receipts: list[Receipt] = []

    async def __aenter__(self) -> "RecallContext":
        return self

    async def __aexit__(self, *_) -> None:
        task = aio.create_task(self.recall())
        if self.wait:
            await task

    def _get_delay(self) -> float:
        if isinstance(self.delay, tuple):
            return random.uniform(*self.delay)
        return self.delay or 0

    def append(self, r: Receipt):
        self.receipts.append(r)

    async def send(
        self,
        message: Union[UniMessage, str],
        target: Union["BaseEvent", Target, None] = None,
        bot: Optional["BaseBot"] = None,
        fallback: bool = True,
        at_sender: Union[str, bool] = False,
        reply_to: Union[str, bool, Reply, None] = False,
        no_wrapper: bool = False,
        **kwargs,
    ) -> None:
        self.append(
            await (
                UniMessage.text(message) if isinstance(message, str) else message
            ).send(
                target=target,
                bot=bot,
                fallback=fallback,
                at_sender=at_sender,
                reply_to=reply_to,
                no_wrapper=no_wrapper,
                **kwargs,
            ),
        )

    @staticmethod
    async def safe_recall(r: Receipt) -> None:
        try:
            await r.recall()
        except Exception as e:
            logger.warning(f"Recall failed: {type(e).__name__}: {e}")
            logger.opt(exception=e).debug("Stack trace:")

    async def recall(self) -> None:
        if not self.receipts:
            return

        receipts = self.receipts.copy()
        self.receipts.clear()

        if self.delay is None:
            await aio.gather(*(self.safe_recall(r) for r in receipts))
        else:
            for r in receipts:
                await aio.sleep(self._get_delay())
                await self.safe_recall(r)
