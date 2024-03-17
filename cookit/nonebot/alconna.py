from nonebot import logger, require

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna.uniseg import Receipt  # noqa: E402


async def captured_recall(r: Receipt):
    try:
        await r.recall()
    except Exception as e:
        logger.warning(f"Recall failed: {type(e).__name__}: {e}")
        logger.opt(exception=e).debug("Stack trace:")
