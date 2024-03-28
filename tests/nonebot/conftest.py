import nonebot
import pytest
from nonebot.adapters.satori import Adapter as SatoriAdapter
from nonebug import NONEBOT_INIT_KWARGS


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi+~websockets+~httpx",
        "log_level": "DEBUG",
    }


@pytest.fixture(scope="session", autouse=True)
def load_adapters(nonebug_init: None):  # noqa: ARG001, PT004
    driver = nonebot.get_driver()
    driver.register_adapter(SatoriAdapter)
