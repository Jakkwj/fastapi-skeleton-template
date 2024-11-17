from funboost import run_forever

from app.tasks.task_test import task_test

if __name__ == "__main__":  # 启动消费
    """
    支持 python 3.11
    运行前设置环境变量, export PYTHONPATH=当前文件夹目录
    python main.py

    multi_process_consume(4)  # 独立开 4 个进程, 每个进程内部使用多线程运行或协程

    传参类型
        只有 str/bool/dict 可以作为参数传递
        bytes 和其它类型好像都不行

    https://funboost.readthedocs.io/zh-cn/latest/articles/c6.html#a
    nb_log_config.py
    LOG_LEVEL_FILTER = logging.INFO  也可在 BoosterParamsMy 中指定
    DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False  # 在控制台是否显示彩色块状的日志。为False则不使用大块的背景颜色。

    关闭启动的多余消息
    https://funboost.readthedocs.io/zh-cn/latest/articles/c6.html#id11
    funboost_config.py
    SHOW_HOW_FUNBOOST_CONFIG_SETTINGS = False
    FUNBOOST_PROMPT_LOG_LEVEL = logging.INFO
    KEEPALIVETIMETHREAD_LOG_LEVEL = logging.INFO

    消费异步任务
    funboost + 全asyncio 编程生态演示: https://funboost.readthedocs.io/zh-cn/latest/articles/c4b.html

    4.30 funboost 远程杀死(取消)任务
    https://funboost.readthedocs.io/zh-cn/latest/articles/c4.html


    3.2 框架支持的函数调度并发模式种类详细介绍
    https://funboost.readthedocs.io/zh-cn/latest/articles/c3.html

    4.6.3 手动设置rpc结果最大等待时间
    https://funboost.readthedocs.io/zh-cn/latest/articles/c4.html
    asio_async_result.set_timeout(3600)  # 最长等待时间 1小时  # 默认 120s

    4.26.2 在多个进程中启动函数的消费, 适合一次启动大量函数的消费或重型任务
    https://funboost.readthedocs.io/zh-cn/latest/articles/c4.html
    sub.multi_process_consume(3) # 独立开3个进程来运行求差函数, 每个进程内部使用多线程运行或协程 来运行求和函数.

    10.2 启动消费后报错: RuntimeError: cannot schedule new futures after interpreter shutdown
    https://funboost.readthedocs.io/zh-cn/latest/articles/c10.html

    解决方法:
        1) run_forever()
        2) multi_process_consume(4)
            一次性启动 4 进程叠加多线程, 此方式需要ctrl + c 关闭 funboost 后必须杀干净后台进程 python.main.py
            否则还是会报错:
            cannot schedule new futures after interpreter shutdown.

    """
    # task_test.consume()

    task_test.multi_process_consume(4)

    run_forever()  # 阻止主线程结束
