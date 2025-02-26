from typing import TYPE_CHECKING

import pytest
from nonebot import on_message
from nonebot.exception import FinishedException, SkippedException
from nonebot.matcher import Matcher

from .utils import FakeMessage, make_fake_event

if TYPE_CHECKING:
    from nonebug import App


async def test_exception_notify(app: "App"):
    from cookit.nonebot.base.tools import exception_notify

    cmd_ev = make_fake_event(_message=FakeMessage("114514"))()

    matcher1 = on_message()

    @matcher1.handle()
    async def _():
        async with exception_notify("err"):
            raise ValueError("test")

    async with app.test_matcher(matcher1) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, cmd_ev)
        ctx.should_call_send(cmd_ev, "err")

    matcher2 = on_message()

    @matcher2.handle()
    async def _(m: Matcher):
        async with exception_notify("err"):
            await m.finish("finished")

    async with app.test_matcher(matcher2) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, cmd_ev)
        ctx.should_call_send(cmd_ev, "finished")
        ctx.should_finished()

    matcher3 = on_message()

    @matcher3.handle()
    async def _():
        async with exception_notify("err", types=(ValueError,)):
            raise ValueError("test")

    async with app.test_matcher(matcher3) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, cmd_ev)
        ctx.should_call_send(cmd_ev, "err")

    matcher4 = on_message()

    @matcher4.handle()
    async def _(m: Matcher):
        with pytest.raises(IndexError):
            async with exception_notify("err", types=(ValueError,)):
                raise IndexError("0")
        await m.finish("err expected")

    async with app.test_matcher(matcher4) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, cmd_ev)
        ctx.should_call_send(cmd_ev, "err expected")
        ctx.should_finished()

    matcher5 = on_message()

    @matcher5.handle()
    async def _(m: Matcher):
        async with exception_notify("err", ignore_nb_exc=False):
            await m.finish("finished")

    async with app.test_matcher(matcher5) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, cmd_ev)
        ctx.should_call_send(cmd_ev, "finished")
        ctx.should_call_send(cmd_ev, "err")

    matcher6 = on_message()

    @matcher6.handle()
    async def _(m: Matcher):
        async with exception_notify(
            "err",
            types=(FinishedException,),
            ignore_nb_exc=False,
        ):
            await m.finish("finished")

    async with app.test_matcher(matcher6) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, cmd_ev)
        ctx.should_call_send(cmd_ev, "finished")
        ctx.should_call_send(cmd_ev, "err")

    matcher7 = on_message()

    @matcher7.handle()
    async def _(m: Matcher):
        async with exception_notify(
            "err",
            types=(SkippedException,),
            ignore_nb_exc=False,
        ):
            await m.finish("finished")

    async with app.test_matcher(matcher7) as ctx:
        bot = ctx.create_bot()
        ctx.receive_event(bot, cmd_ev)
        ctx.should_call_send(cmd_ev, "finished")
        ctx.should_finished()
