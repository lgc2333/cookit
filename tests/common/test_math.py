from datetime import timedelta


def test_auto_convert_unit():
    from cookit import auto_convert_unit

    assert auto_convert_unit(["m", "km"], multiplier=1000, value=5000) == "5.00 km"
    assert (
        auto_convert_unit(
            ["m", "km"],
            multiplier=1000,
            value=5000,
            round_n=0,
            with_space=False,
        )
        == "5km"
    )
    assert (
        auto_convert_unit(
            ["s", "min(s)", "hr(s)"],
            multiplier=60,
            value=3600,
            round_n=1,
            suffix="/it",
            with_space=False,
            unit_index=1,
        )
        == "1.0hr(s)/it"
    )
    assert (
        auto_convert_unit(
            ["b", "k", "m", "g"],
            multiplier=1024,
            value=1000,
            round_n=2,
            with_space=False,
            unit_threshold=1000,
        )
        == "0.98k"
    )
    assert (
        auto_convert_unit(
            ["b", "k", "m", "g"],
            multiplier=1024,
            value=1024,
            round_n=1,
            suffix="/s",
            with_space=True,
            unit_threshold=1000,
        )
        == "1.0 k/s"
    )


td_full = timedelta(days=1, hours=2, minutes=3, seconds=4, milliseconds=5)
td_no_day = timedelta(hours=2, minutes=3, seconds=4, milliseconds=5)
td_zero = timedelta()


def test_format_timedelta():
    from cookit import (
        TimeUnit,
        format_timedelta,
        format_timedelta_human_en,
        format_timedelta_human_en_spc,
        format_timedelta_human_zh,
        format_timedelta_human_zh_spc,
    )

    # normal
    assert format_timedelta(td_full) == "1:02:03:04"
    assert format_timedelta(td_full, with_ms=True) == "1:02:03:04.005"
    assert format_timedelta(td_full, with_ms=True, ms_num=1) == "1:02:03:04.0"
    assert format_timedelta(td_full, with_ms=True, ms_num=None) == "1:02:03:04.5"
    assert format_timedelta(td_full, pad_day=True) == "01:02:03:04"
    assert format_timedelta(td_full, pad_day=True, day_pad_num=3) == "001:02:03:04"
    assert format_timedelta(td_full, pad_time=False) == "1:2:3:4"
    assert format_timedelta(td_full, pad_time_first=False) == "1:2:03:04"
    assert format_timedelta(td_full, pad_time=False, pad_time_first=False) == "1:2:3:4"
    assert (
        format_timedelta(td_full, unit_up_to=TimeUnit.HOUR, with_ms=True)
        == "26:03:04.005"
    )
    assert (
        format_timedelta(td_full, unit_up_to=TimeUnit.MINUTE, with_ms=True)
        == "1563:04.005"
    )
    assert (
        format_timedelta(td_full, unit_up_to=TimeUnit.SECOND, with_ms=True)
        == "93784.005"
    )
    assert (
        format_timedelta(td_full, unit_up_to=TimeUnit.MILLISECOND, with_ms=True)
        == "93784005"
    )

    # no day
    assert format_timedelta(td_no_day) == "02:03:04"
    assert format_timedelta(td_no_day, with_ms=True) == "02:03:04.005"
    assert format_timedelta(td_no_day, with_ms=True) == "02:03:04.005"
    assert format_timedelta(td_no_day, pad_time_first=False) == "2:03:04"
    assert (
        format_timedelta(td_no_day, with_ms=True, with_empty_day=True)
        == "0:02:03:04.005"
    )

    # zero
    assert (
        format_timedelta(td_zero, with_ms=True, with_empty_day=True) == "0:00:00:00.000"
    )

    # human
    assert format_timedelta_human_en(td_full, with_ms=True) == "1d2h3m4s5ms"
    assert format_timedelta_human_en_spc(td_full, with_ms=False) == "1d 2h 3m 4s"
    assert format_timedelta_human_zh(td_full, with_ms=False) == "1天2时3分4秒"
    assert (
        format_timedelta_human_zh_spc(td_full, with_ms=True) == "1天 2时 3分 4秒 5毫秒"
    )
