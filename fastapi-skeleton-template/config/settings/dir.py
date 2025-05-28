from functools import cache
from os import path


@cache
def get_work_dir() -> str:
    """获取 fastapi 的绝对路径.
    必须提前通过绝对路径方式锁定, 因为实际计算中会更改 工作路径

    Returns:
        current_dir: /fastapi-skeleton-template/config/
        work_dir: /fastapi-skeleton-template/
    """
    current_dir: str = __file__.strip(path.basename(__file__))  # 当前文件所在的绝对路径
    return current_dir.replace("config/settings/", "").replace(
        "config\\settings\\", ""
    )  # 必须提前确定
