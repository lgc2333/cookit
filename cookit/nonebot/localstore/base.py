from nonebot import get_plugin_config
from nonebot_plugin_localstore import plugin_config as localstore_config
from pydantic import BaseModel, Field


class LocalStoreConfigModel(BaseModel):
    sure: bool = Field(
        default=False,
        alias="i_am_sure_i_want_to_use_default_localstore_file_path",
    )


LOCALSTORE_DEFAULT_PATH_WARNING_MSG = (
    "\nWarning:"
    "\n"
    "\nDetected that the `localstore` plugin is using default storage locations:"
    "\n- On Windows:"
    "\n    C:\\Users\\<username>\\AppData\\Local (and Roaming)\\nonebot2"
    "\n- On Linux:"
    "\n    ~/.cache/nonebot2, ~/.config/nonebot2, and ~/.local/share/nonebot2"
    "\n- On macOS:"
    "\n    ~/Library/Caches/nonebot2 and ~/Library/Application Support/nonebot2"
    "\n"
    "\nI strongly dislike this default storage approach as it:"
    "\n- Increases complexity when migrating NoneBot instances"
    "\n- May cause data conflicts when running multiple NoneBot instances simultaneously"
    "\nTherefore, this plugin will REFUSE TO LOAD."
    "\n"
    "\nRecommend to add this configuration"
    " to let localstore plugin store data in the current working directory:"
    "\n- LOCALSTORE_USE_CWD=True"
    "\nOr edit your configuration file according to localstore plugin's documentation"
    " to configure custom storage paths"
    "\n"
    "\nIf you insist on using default storage paths,"
    " add this configuration to ignore this error:"
    "\n- I_AM_SURE_I_WANT_TO_USE_DEFAULT_LOCALSTORE_FILE_PATH=True"
    "\n"
    "\n警告："
    "\n"
    "\n检测到 `localstore` 插件正在使用默认的文件存放位置，即："
    "\n- 在 Windows 系统下："
    "\n    C:\\Users\\<username>\\AppData\\Local (及 Roaming)\\nonebot2"
    "\n- 在 Linux 系统下："
    "\n    ~/.cache/nonebot2 与 ~/.config/nonebot2 与 ~/.local/share/nonebot2"
    "\n- 在 macOS 系统下："
    "\n    ~/Library/Caches/nonebot2 与 ~/Library/Application Support/nonebot2"
    "\n"
    "\n由于本人极不喜欢 localstore 插件这样存放数据文件，"
    "\n这不仅增加了用户迁移 NoneBot 实例的复杂程度，"
    "\n而且在同时运行多个 NoneBot 实例的情况下还可能会导致实例间数据冲突。"
    "\n因此，本插件将 拒绝加载。"
    "\n"
    "\n建议添加下方配置项使 localstore 插件在当前工作目录下存储数据："
    "\n- LOCALSTORE_USE_CWD=True"
    "\n或者参考其文档自行修改配置使用其他文件夹作为数据存储位置。"
    "\n"
    "\n如果你坚决要使用 localstore 插件的默认文件存放位置，请添加以下配置项以忽略本错误："
    "\n- I_AM_SURE_I_WANT_TO_USE_DEFAULT_LOCALSTORE_FILE_PATH=True"
)


def ensure_localstore_path_config():
    if not (
        localstore_config.localstore_use_cwd
        or localstore_config.localstore_cache_dir
        or localstore_config.localstore_config_dir
        or localstore_config.localstore_data_dir
        or get_plugin_config(LocalStoreConfigModel).sure
    ):
        raise RuntimeError(LOCALSTORE_DEFAULT_PATH_WARNING_MSG)
