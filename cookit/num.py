from functools import partial
from typing import Optional, Sequence

BYTE_UNITS = ["B", "K", "M", "G", "T", "P"]
BYTE_B_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def auto_convert_unit(
    units: Sequence[str],
    multiplier: int,
    value: float,
    round_n: int = 2,
    suffix: str = "",
    with_space: bool = True,
    unit_index: int = 0,
    unit_threshold: Optional[int] = None,
) -> str:
    if unit_threshold is None:
        unit_threshold = multiplier
    units = units[unit_index:]
    if not units:
        raise ValueError("Wrong `unit_index`")

    unit = None
    for x in units:
        if value < unit_threshold:
            unit = x
            break
        value /= multiplier
    return (
        f"{value:.{round_n}f}"
        f"{' ' if with_space else ''}"
        f"{unit or units[-1]}"
        f"{suffix}"
    )


auto_convert_byte = partial(
    auto_convert_unit,
    units=BYTE_UNITS,
    multiplier=1024,
    unit_threshold=1000,
)
auto_convert_byte_speed = partial(
    auto_convert_unit,
    units=BYTE_UNITS,
    multiplier=1024,
    suffix="/s",
    unit_threshold=1000,
)
auto_convert_byte_b = partial(
    auto_convert_unit,
    units=BYTE_B_UNITS,
    multiplier=1024,
    unit_threshold=1000,
)
auto_convert_byte_b_speed = partial(
    auto_convert_unit,
    units=BYTE_B_UNITS,
    multiplier=1024,
    suffix="/s",
    unit_threshold=1000,
)
