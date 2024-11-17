from collections.abc import Callable

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from funboost import RemoteTaskKiller


async def push_task(publisher: Callable, **kwargs) -> str:
    """发布 funboost 任务.
    不记录 task_id, 超时时间默认为 120s, 无法杀死.
    """
    asio_async_result = await publisher.aio_push(**kwargs)  # type: ignore  发布 funboost 异步任务
    result: str = await asio_async_result.result

    return result


async def publish_task(task_name: str, publisher: Callable, request: Request, **kwargs) -> str:
    """发布 funboost 任务.
    首先通过 redis 记录 task_id, task_id 用于判断此任务是否还在运行中, 从而 stop 的时候可以放回准确的信息
    然后发布任务, 并设置最大时间
    成功返回结果后清空 redis

    注意不要用 aio_publish, 虽然 aio_publish 可以设定 task_id, 但是会立刻放回结果 (暂时 2024.09.17 不知道如何 await)
    """
    asio_async_result = await publisher.aio_push(**kwargs)  # type: ignore  发布 funboost 异步任务
    asio_async_result.set_timeout(3600)  # 最长等待时间 1小时, 默认 120s
    await request.app.redis.set(task_name, asio_async_result.task_id)
    result: str = await asio_async_result.result
    await request.app.redis.delete(task_name)

    return result


async def kill_task(task_name: str, publisher: Callable, request: Request) -> ORJSONResponse:
    """杀死 funboost 任务.
    funboost 远程杀死任务: https://funboost.readthedocs.io/zh-cn/latest/articles/c4.html
    杀死后, 删除 redis 中的 task_name
    """
    task_id: str = await request.app.redis.get(task_name)

    if task_id:
        RemoteTaskKiller(publisher.queue_name, task_id).send_kill_remote_task_comd()  # type: ignore 根据 task_name 远程杀死任务
        await request.app.redis.delete(task_name)

        return ORJSONResponse(
            {"message": "Saving has been stopped."}, status_code=status.HTTP_410_GONE
        )

    return ORJSONResponse({"message": "Nothing is saving."}, status_code=status.HTTP_200_OK)
