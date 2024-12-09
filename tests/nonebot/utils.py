# https://github.com/nonebot/nonebot2/blob/master/tests/utils.py

from collections.abc import Iterable, Mapping
from typing import Optional, Union
from typing_extensions import override

from nonebot.adapters import Event, Message, MessageSegment
from pydantic import create_model


class FakeMessageSegment(MessageSegment["FakeMessage"]):
    @classmethod
    @override
    def get_message_class(cls):
        return FakeMessage

    @override
    def __str__(self) -> str:
        return self.data["text"] if self.type == "text" else f"[fake:{self.type}]"

    @classmethod
    def text(cls, text: str):
        return cls("text", {"text": text})

    @staticmethod
    def image(url: str):
        return FakeMessageSegment("image", {"url": url})

    @staticmethod
    def nested(content: "FakeMessage"):
        return FakeMessageSegment("node", {"content": content})

    @override
    def is_text(self) -> bool:
        return self.type == "text"


class FakeMessage(Message[FakeMessageSegment]):
    @classmethod
    @override
    def get_segment_class(cls):
        return FakeMessageSegment

    @staticmethod
    @override
    def _construct(msg: Union[str, Iterable[Mapping]]):
        if isinstance(msg, str):
            yield FakeMessageSegment.text(msg)
        else:
            for seg in msg:
                yield FakeMessageSegment(**seg)


def make_fake_event(
    _base: Optional[type[Event]] = None,
    _type: str = "message",
    _name: str = "test",
    _description: str = "test",
    _user_id: Optional[str] = "test",
    _session_id: Optional[str] = "test",
    _message: Optional[Message] = None,
    _to_me: bool = True,
    **fields,
) -> type[Event]:
    Base = _base or Event  # noqa: N806

    class FakeEvent(Base):
        @override
        def get_type(self) -> str:
            return _type

        @override
        def get_event_name(self) -> str:
            return _name

        @override
        def get_event_description(self) -> str:
            return _description

        @override
        def get_user_id(self) -> str:
            if _user_id is not None:
                return _user_id
            raise NotImplementedError

        @override
        def get_session_id(self) -> str:
            if _session_id is not None:
                return _session_id
            raise NotImplementedError

        @override
        def get_message(self) -> "Message":
            if _message is not None:
                return _message
            raise NotImplementedError

        @override
        def is_tome(self) -> bool:
            return _to_me

    return create_model("FakeEvent", __base__=FakeEvent, **fields)
