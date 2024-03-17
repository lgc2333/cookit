from datetime import timedelta
from enum import IntEnum
from functools import partial
from typing import Any, Optional, Sequence


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


BYTE_UNITS = ["B", "K", "M", "G", "T", "P"]
BYTE_B_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]

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


class TimeUnit(IntEnum):
    MILLISECOND = 0
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4


def format_timedelta(
    t: timedelta,
    unit_up_to: TimeUnit = TimeUnit.DAY,
    with_ms: bool = False,
    with_empty_day: bool = False,
    day_divider: str = ":",
    time_divider: str = ":",
    ms_divider: str = ".",
    day_suffix: str = "",
    hour_suffix: str = "",
    minute_suffix: str = "",
    second_suffix: str = "",
    ms_suffix: str = "",
    pad_day: bool = False,
    pad_time: bool = True,
    pad_time_first: bool = True,
    day_pad_num: int = 2,
    ms_num: Optional[int] = 3,
) -> str:
    mm, ss = divmod(t.seconds, 60)
    hh, mm = divmod(mm, 60)
    ms = t.microseconds // 1000

    d_str = ""
    h_str = ""
    m_str = ""
    s_str = ""
    ms_str = ""

    should_pad_next_time = pad_time_first

    def pad_t(x: Any) -> str:
        nonlocal should_pad_next_time
        if not pad_time:
            return f"{x}"
        if not should_pad_next_time:
            should_pad_next_time = True
            return f"{x}"
        return f"{x:02d}"

    if t.days or with_empty_day:
        if unit_up_to >= TimeUnit.DAY:
            dd = f"{t.days:0{day_pad_num}d}" if pad_day else f"{t.days}"
            d_str = f"{dd}{day_suffix}{day_divider}"
        else:
            hh += t.days * 24

    if unit_up_to >= TimeUnit.HOUR:
        h_str = f"{pad_t(hh)}{hour_suffix}{time_divider}"
    elif hh:
        mm += hh * 60

    if unit_up_to >= TimeUnit.MINUTE:
        m_str = f"{pad_t(mm)}{minute_suffix}{time_divider}"
    elif mm:
        ss += mm * 60

    if unit_up_to >= TimeUnit.SECOND:
        s_str = f"{pad_t(ss)}{second_suffix}"
    elif ss:
        ms += ss * 1000

    if unit_up_to is TimeUnit.MILLISECOND:
        with_ms = True
        ms_divider = ""

    if with_ms and ms_num != 0:
        ms = ms if ((ms_num is None) or (ms >= 1000)) else f"{ms:03d}"[:ms_num]
        ms_str = f"{ms_divider}{ms}{ms_suffix}"

    return f"{d_str}{h_str}{m_str}{s_str}{ms_str}"


TIMEDELTA_NO_PAD = {
    "pad_day": False,
    "pad_time": False,
    "ms_num": None,
}
TIMEDELTA_EMPTY_DIVIDER = {
    "day_divider": "",
    "time_divider": "",
    "ms_divider": "",
}
TIMEDELTA_SPACE_DIVIDER = {
    "day_divider": " ",
    "time_divider": " ",
    "ms_divider": " ",
}
TIMEDELTA_SUFFIX_EN = {
    "day_suffix": "d",
    "hour_suffix": "h",
    "minute_suffix": "m",
    "second_suffix": "s",
    "ms_suffix": "ms",
}
TIMEDELTA_SUFFIX_ZH = {
    "day_suffix": "天",
    "hour_suffix": "时",
    "minute_suffix": "分",
    "second_suffix": "秒",
    "ms_suffix": "毫秒",
}

format_timedelta_human_en = partial(
    format_timedelta,
    **TIMEDELTA_NO_PAD,
    **TIMEDELTA_EMPTY_DIVIDER,
    **TIMEDELTA_SUFFIX_EN,
)
format_timedelta_human_en_spc = partial(
    format_timedelta,
    **TIMEDELTA_NO_PAD,
    **TIMEDELTA_SPACE_DIVIDER,
    **TIMEDELTA_SUFFIX_EN,
)
format_timedelta_human_zh = partial(
    format_timedelta,
    **TIMEDELTA_NO_PAD,
    **TIMEDELTA_EMPTY_DIVIDER,
    **TIMEDELTA_SUFFIX_ZH,
)
format_timedelta_human_zh_spc = partial(
    format_timedelta,
    **TIMEDELTA_NO_PAD,
    **TIMEDELTA_SPACE_DIVIDER,
    **TIMEDELTA_SUFFIX_ZH,
)
