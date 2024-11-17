from threading import Lock
from traceback import format_exc

from funboost import boost
from loguru import logger

from .params import BoosterParamsMy


@boost(BoosterParamsMy(queue_name="task_test"))
async def task_test():
    """消费异步任务.
    此函数必须通过 multi_process_consume 进行消费
    否则会报错: cannot schedule new futures after interpreter shutdown.

    注意重启 funboost 必须杀干净后台进程 python.main.py
    否则 task_test 还是会报错:
    cannot schedule new futures after interpreter shutdown.

    解决方法:
        1) run_forever()
        2)multi_process_consume(4)  # 一次性启动 4 进程叠加多线程

    """
    lock = Lock()

    try:
        with lock:  # 防止杀死函数后的锁不释放
            logger.info("funboost test task...")

    except Exception:
        return format_exc()
