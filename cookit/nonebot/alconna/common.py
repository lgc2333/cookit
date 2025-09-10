from nonebot.adapters import Message as BaseMessage
from nonebot_plugin_alconna.uniseg import Reply, UniMessage


def extract_reply_msg(msg: UniMessage) -> UniMessage | None:
    if (
        Reply in msg
        and isinstance((reply_raw := msg[Reply, 0].msg), BaseMessage)
        and (reply_msg := UniMessage.of(message=reply_raw))
    ):
        return reply_msg
    return None
