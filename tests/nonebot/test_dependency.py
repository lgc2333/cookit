from typing import TYPE_CHECKING

from .utils import FakeMessage, make_fake_event

if TYPE_CHECKING:
    from nonebug import App


async def test_command_arg_plaintext(app: "App"):
    from cookit.nonebot import CommandArgPlaintext
    from nonebot import on_command
    from nonebot.matcher import Matcher

    ev = make_fake_event(_message=FakeMessage("/test resp1\n"))()
    ev_empty = make_fake_event(_message=FakeMessage("/test"))()

    matcher1 = on_command("test")

    @matcher1.handle()
    async def _(m: Matcher, arg: str = CommandArgPlaintext()):
        await m.finish(arg)

    async with app.test_matcher(matcher1) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, ev)
        ctx.should_call_send(ev, "resp1")
        ctx.receive_event(bot, ev_empty)
        ctx.should_call_send(ev_empty, "")

    matcher2 = on_command("test")

    @matcher2.handle()
    async def _(m: Matcher, arg: str = CommandArgPlaintext(strip=False)):
        await m.finish(arg)

    async with app.test_matcher(matcher2) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, ev)
        ctx.should_call_send(ev, "resp1\n")
        ctx.receive_event(bot, ev_empty)
        ctx.should_call_send(ev_empty, "")

    matcher3 = on_command("test")

    @matcher3.handle()
    async def _(m: Matcher, arg: str = CommandArgPlaintext(allow_empty=False)):
        await m.finish(arg)

    @matcher3.handle()
    async def _(m: Matcher):
        await m.finish("empty arg")

    async with app.test_matcher(matcher3) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, ev)
        ctx.should_call_send(ev, "resp1")
        ctx.receive_event(bot, ev_empty)
        ctx.should_call_send(ev_empty, "empty arg")
