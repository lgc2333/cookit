import pytest


def pytest_configure(config: pytest.Config) -> None:
    from nonebug import NONEBOT_INIT_KWARGS

    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi+~websockets+~httpx",
        "log_level": "DEBUG",
    }


@pytest.fixture(scope="session", autouse=True)
def load_adapters(nonebug_init: None):  # noqa: ARG001, PT004
    from nonebot import get_driver
    from nonebot.adapters.satori import Adapter as SatoriAdapter

    driver = get_driver()
    driver.register_adapter(SatoriAdapter)
