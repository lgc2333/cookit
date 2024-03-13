from typing import Callable, Optional, TypeVar, Union

TA = TypeVar("TA")
TB = TypeVar("TB")


def qor(a: Optional[TA], b: Union[TB, Callable[[], TB]]) -> Union[TA, TB]:
    return a if (a is not None) else (b() if isinstance(b, Callable) else b)
