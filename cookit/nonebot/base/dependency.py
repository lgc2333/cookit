from typing import Any

from nonebot.adapters import Message as BaseMessage
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Depends

from ... import copy_func_arg_annotations


def dep_command_arg_plaintext(strip: bool = True, allow_empty: bool = True):
    async def dep(arg: BaseMessage = CommandArg()) -> str:
        t = arg.extract_plain_text()
        if strip:
            t = t.strip()
        if not allow_empty and not t:
            Matcher.skip()
        return t

    return dep


@copy_func_arg_annotations(dep_command_arg_plaintext)
def CommandArgPlaintext(*args, **kwargs) -> Any:  # noqa: N802
    return Depends(dep_command_arg_plaintext(*args, **kwargs))
