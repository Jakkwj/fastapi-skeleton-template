from funboost import (
    BoosterParams,
    BrokerEnum,
    ConcurrentModeEnum,
)


class BoosterParamsMy(BoosterParams):
    """funboost 的入参.
    LOG_PATH 必须在 nb_log_config.py 中指定

    4.0.5 自定义子类继承 BoosterParams,使得每次少传参
    https://funboost.readthedocs.io/zh-cn/latest/articles/c4.html
    """

    broker_kind: str = BrokerEnum.REDIS
    is_using_rpc_mode: bool = True  # 是否使用rpc模式, 可以在发布端获取消费端的结果回调, 但消耗一定性能, 使用async_result.result时候会等待阻塞住当前线程
    is_support_remote_kill_task: bool = True  # 是否支持远程任务杀死功能, 如果任务数量少, 单个任务耗时长, 确实需要远程发送命令来杀死正在运行的函数, 才设置为true, 否则不建议开启此功能
    concurrent_mode: str = (
        ConcurrentModeEnum.THREADING
    )  # 线程方式运行, 兼容支持 async def 的异步函数, 默认值
    concurrent_num: int = 200  # 并发数量, 默认 50
