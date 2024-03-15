# generated by copilot
# ruff: noqa: E731

from cookit.common import qor


def test_qor_with_a_not_none():
    a = 5
    b = 10
    result = qor(a, b)
    assert result == a


def test_qor_with_a_none_and_b_not_callable():
    a = None
    b = 10
    result = qor(a, b)
    assert result == b


def test_qor_with_a_none_and_b_callable():
    a = None
    b = lambda: 10
    result = qor(a, b)
    assert result == b()