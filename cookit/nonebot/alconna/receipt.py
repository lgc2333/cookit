import asyncio as aio
import random
from typing import TYPE_CHECKING, Optional, Union
from typing_extensions import Self

from nonebot import logger
from nonebot_plugin_alconna.uniseg import Receipt, Reply, Target, UniMessage

if TYPE_CHECKING:
    from nonebot.adapters import Bot as BaseBot, Event as BaseEvent


class RecallContext:
    def __init__(
        self,
        delay: float | tuple[float, float] | None = None,
        wait: bool = False,
    ) -> None:
        """Create a context that records sent receipts for later recall."""
        self.delay = delay
        self.wait = wait
        self.receipts: list[Receipt] = []

    async def __aenter__(self) -> Self:
        """Enter the recall collection context."""
        return self

    async def __aexit__(self, *_) -> None:
        """Schedule or await message recall when leaving the context."""
        task = aio.create_task(self.recall())
        if self.wait:
            await task

    def _get_delay(self) -> float:
        """Resolve the configured recall delay, including random ranges."""
        if isinstance(self.delay, tuple):
            return random.uniform(*self.delay)
        return self.delay or 0

    def append(self, r: Receipt):
        """Record a receipt for later recall."""
        self.receipts.append(r)

    async def send(
        self,
        message: UniMessage | str,
        target: Union["BaseEvent", Target, None] = None,
        bot: Optional["BaseBot"] = None,
        fallback: bool = True,
        at_sender: str | bool = False,
        reply_to: str | bool | Reply | None = False,
        no_wrapper: bool = False,
        **kwargs,
    ) -> None:
        """Send a UniMessage or text and record its receipt for recall."""
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
        """Recall one receipt and log failures instead of raising them."""
        try:
            await r.recall()
        except Exception as e:
            logger.warning(f"Recall failed: {type(e).__name__}: {e}")
            logger.opt(exception=e).debug("Stack trace:")

    async def recall(self) -> None:
        """Recall all recorded receipts immediately or with configured delays."""
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
