from typing import TYPE_CHECKING

from nonebot import on_message

from .utils import FakeMessage, make_fake_event

if TYPE_CHECKING:
    from nonebug import App


async def test_extract_reply_msg_returns_unimessage_from_base_message_reply(
    app: "App",  # noqa: ARG001
):
    from nonebot import require

    require("nonebot_plugin_alconna")

    from cookit.nonebot.alconna import extract_reply_msg
    from nonebot_plugin_alconna.uniseg import Reply, UniMessage

    ev = make_fake_event(_message=FakeMessage("test"))()
    matcher = on_message()

    @matcher.handle()
    async def _():
        reply = Reply("reply-id", FakeMessage("hello"))
        message = UniMessage([reply])
        result = extract_reply_msg(message)
        assert result is not None
        assert result.extract_plain_text() == "hello"

    async with app.test_matcher(matcher) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, ev)


def test_extract_reply_msg_returns_none_without_base_message_reply(
    app: "App",  # noqa: ARG001
):
    from nonebot import require

    require("nonebot_plugin_alconna")

    from cookit.nonebot.alconna import extract_reply_msg
    from nonebot_plugin_alconna.uniseg import Reply, UniMessage

    assert extract_reply_msg(UniMessage.text("hello")) is None
    assert extract_reply_msg(UniMessage([Reply("reply-id", "plain")])) is None
