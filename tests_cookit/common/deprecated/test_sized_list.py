import pytest

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


def test_sized_list_keeps_latest_items_after_initialization():
    from cookit.common.deprecated import SizedList

    items = SizedList([1, 2, 3], size=2)

    assert items == [2, 3]
    assert items.last == 3


def test_sized_list_without_size_does_not_drop_items():
    from cookit.common.deprecated import SizedList

    items = SizedList([1, 2], size=None)
    items.append(3)

    assert items == [1, 2, 3]


def test_sized_list_append_extend_and_insert_respect_size():
    from cookit.common.deprecated import SizedList

    items = SizedList[int](size=3)

    items.append(1)
    items.extend([2, 3, 4])
    items.insert(0, 0)

    assert items == [2, 3, 4]
    assert items.last == 4


def test_sized_list_add_returns_new_sized_list_with_same_size():
    from cookit.common.deprecated import SizedList

    items = SizedList([1, 2], size=3)

    result = items + [3, 4]  # noqa: RUF005

    assert isinstance(result, SizedList)
    assert result == [2, 3, 4]
    assert result.size == 3
    assert items == [1, 2]


def test_sized_list_iadd_mutates_in_place_and_returns_self():
    from cookit.common.deprecated import SizedList

    items = SizedList([1], size=2)

    result = items
    result += [2, 3]

    assert result is items
    assert items == [2, 3]


def test_sized_list_last_is_none_when_empty():
    from cookit.common.deprecated import SizedList

    assert SizedList[int]().last is None
