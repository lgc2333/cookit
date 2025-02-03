import sys
from typing import Any, Generic, TypeVar, overload
from typing_extensions import override

T = TypeVar("T")

if sys.version_info >= (3, 10):
    from contextlib import nullcontext as nullcontext

else:
    from contextlib import AbstractAsyncContextManager, AbstractContextManager

    class nullcontext(AbstractContextManager, AbstractAsyncContextManager, Generic[T]):  # noqa: N801
        @overload
        def __init__(self: "nullcontext[None]") -> None: ...
        @overload
        def __init__(self, enter_result: T) -> None: ...
        def __init__(self, enter_result: Any = None):
            super().__init__()
            self.enter_result: T = enter_result

        @override
        def __enter__(self):
            return self.enter_result

        @override
        def __exit__(self, *_):
            pass

        @override
        async def __aenter__(self):
            return self.enter_result

        @override
        async def __aexit__(self, *_):
            pass
