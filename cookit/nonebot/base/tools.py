from contextlib import asynccontextmanager

from nonebot import logger
from nonebot.exception import MatcherException, ProcessException
from nonebot.matcher import current_matcher


@asynccontextmanager
async def exception_notify(
    msg: str,
    log_msg: str | None = None,
    types: tuple[type[BaseException]] | None = None,
    ignore_nb_exc: bool = True,
):
    try:
        yield
    except Exception as e:
        if (types and (not isinstance(e, types))) or (
            ignore_nb_exc and isinstance(e, ProcessException | MatcherException)
        ):
            raise
        msg = msg.format(e=str(e), type=type(e).__name__)
        log_msg = log_msg.format(e=str(e), type=type(e).__name__) if log_msg else msg
        logger.opt(depth=2).exception(log_msg)
        await current_matcher.get().finish(msg)
    return  # noqa: PLR1711
