from typing import Optional, Sequence

import pytest
from cookit.num import auto_convert_unit


@pytest.mark.parametrize(
    (
        "units",
        "multiplier",
        "value",
        "round_n",
        "suffix",
        "with_space",
        "unit_index",
        "unit_threshold",
        "expected",
    ),
    [
        (["m", "km"], 1000, 5000, 2, "", True, 0, None, "5.00 km"),
        (["s", "min(s)", "hr(s)"], 60, 3600, 1, "/it", False, 1, None, "1.0hr(s)/it"),
        (["b", "k", "m", "g"], 1024, 1000, 2, "", False, 0, 1000, "0.98k"),
        (["b", "k", "m", "g"], 1024, 1024, 1, "/s", True, 0, 1000, "1.0 k/s"),
    ],
)
def test_auto_convert_unit(
    units: Sequence[str],
    multiplier: int,
    value: float,
    round_n: int,
    suffix: str,
    with_space: bool,
    unit_index: int,
    unit_threshold: Optional[int],
    expected: str,
):
    assert (
        auto_convert_unit(
            units,
            multiplier,
            value,
            round_n,
            suffix,
            with_space,
            unit_index,
            unit_threshold,
        )
        == expected
    )
