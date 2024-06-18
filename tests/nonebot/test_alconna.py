import time
from typing import TYPE_CHECKING, Any
from typing_extensions import override

from nonebot.adapters.satori.models import LoginStatus

if TYPE_CHECKING:
    from nonebot.adapters.satori import Adapter as SatoriAdapter
    from nonebug import App
    from nonebug.mixin.process import MatcherContext


def create_fake_satori_adapter(ctx: "MatcherContext") -> "SatoriAdapter":
    from nonebot import get_driver
    from nonebot.adapters import Bot as BaseBot
    from nonebot.adapters.satori import Adapter as SatoriAdapter

    class FakeAdapter(SatoriAdapter):
        @override
        async def _call_api(self, bot: BaseBot, api: str, **data) -> Any:
            return ctx.got_call_api(self, api, **data)

    return FakeAdapter(get_driver())


async def test_captured_recall(app: "App"):
    from nonebot import on_message, require
    from nonebot.adapters.satori import Bot as SatoriBot
    from nonebot.adapters.satori.config import ClientInfo
    from nonebot.adapters.satori.event import MessageCreatedEvent
    from nonebot.adapters.satori.models import ChannelType, Login, MessageObject, User
    from nonebot.compat import type_validate_python

    require("nonebot_plugin_alconna")

    from cookit.nonebot.alconna import RecallContext
    from nonebot_plugin_alconna.uniseg import UniMessage

    matcher = on_message()

    @matcher.handle()
    async def _():
        async with RecallContext(delay=0, wait=True) as recall:
            await recall.send(UniMessage("world!"))
            recall.append(await UniMessage("world!").send())

    async with app.test_matcher(matcher) as ctx:
        adapter = create_fake_satori_adapter(ctx)
        bot = ctx.create_bot(
            base=SatoriBot,
            adapter=adapter,
            self_id="fake_bot",
            login=Login(
                user=User(id="fake_user"),
                platform="fake",
                self_id="fake_bot",
                status=LoginStatus.ONLINE,
            ),
            info=ClientInfo(port=14514),
        )
        event = type_validate_python(
            MessageCreatedEvent,
            {
                "id": 114514,
                "type": "message-created",
                "platform": "fake",
                "self_id": "fake_bot",
                "timestamp": int(time.time() * 1000),
                "channel": {"id": "fake_channel", "type": ChannelType.TEXT},
                "user": {"id": "fake_user"},
                "message": {"id": "fake_message", "content": "hello"},
            },
        )
        ctx.receive_event(bot, event)

        ctx.should_call_api(
            "message_create",
            {"channel_id": "fake_channel", "content": "world!"},
            [MessageObject(id="114515", content="world!")],
        )
        ctx.should_call_api(
            "message_create",
            {"channel_id": "fake_channel", "content": "world!"},
            [MessageObject(id="114516", content="world!")],
        )
        ctx.should_call_api(
            "message_delete",
            {"channel_id": "fake_channel", "message_id": "114515"},
        )
        ctx.should_call_api(
            "message_delete",
            {"channel_id": "fake_channel", "message_id": "114516"},
        )
