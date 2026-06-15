from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest
    from nonebug import App


class FakeReceipt:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.recall_count = 0

    async def recall(self):
        self.recall_count += 1
        if self.fail:
            raise RuntimeError("recall failed")


async def test_recall_context_returns_self_and_noops_without_receipts(
    app: "App",  # noqa: ARG001
):
    from nonebot import require

    require("nonebot_plugin_alconna")
    from cookit.nonebot.alconna import RecallContext

    async with RecallContext(wait=True) as recall:
        assert isinstance(recall, RecallContext)

    assert recall.receipts == []


async def test_recall_context_recalls_all_receipts_without_delay(
    app: "App",  # noqa: ARG001
):
    from nonebot import require

    require("nonebot_plugin_alconna")
    from cookit.nonebot.alconna import RecallContext

    receipt_a = FakeReceipt()
    receipt_b = FakeReceipt()
    recall = RecallContext()
    recall.append(receipt_a)  # type: ignore[arg-type]
    recall.append(receipt_b)  # type: ignore[arg-type]

    await recall.recall()

    assert receipt_a.recall_count == 1
    assert receipt_b.recall_count == 1
    assert recall.receipts == []


async def test_recall_context_uses_tuple_delay(
    app: "App",  # noqa: ARG001
    monkeypatch: "pytest.MonkeyPatch",
):
    from nonebot import require

    require("nonebot_plugin_alconna")
    from cookit.nonebot.alconna import RecallContext, receipt as receipt_module

    monkeypatch.setattr(receipt_module.random, "uniform", lambda _start, end: end)
    sleeps: list[float] = []

    async def fake_sleep(delay: float):
        sleeps.append(delay)

    monkeypatch.setattr(receipt_module.aio, "sleep", fake_sleep)
    receipt = FakeReceipt()
    recall = RecallContext(delay=(1, 2))
    recall.append(receipt)  # type: ignore[arg-type]

    await recall.recall()

    assert sleeps == [2]
    assert receipt.recall_count == 1


async def test_recall_context_logs_failed_recall(app: "App"):  # noqa: ARG001
    from nonebot import require

    require("nonebot_plugin_alconna")
    from cookit.nonebot.alconna import RecallContext

    receipt = FakeReceipt(fail=True)

    await RecallContext.safe_recall(receipt)  # type: ignore[arg-type]

    assert receipt.recall_count == 1
