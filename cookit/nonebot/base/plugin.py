from nonebot.plugin import get_plugin


def assert_plugin_loaded(name: str):
    if get_plugin(name) is None:
        raise ImportError(f"You should require plugin `{name}` first!")
