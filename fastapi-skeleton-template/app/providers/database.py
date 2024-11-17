from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from config.config import get_settings

settings = get_settings()


""" 异步引擎

https://blog.csdn.net/meisanggou/article/details/104427146

pool_size
设置连接池中, 保持的连接数. 初始化时, 并不产生连接. 只有慢慢需要连接时, 才会产生连接. 例如我们的连接数设置成pool_size=10. 如果我们的并发量一直最高是5. 那么我们的连接池里的连接数也就是5. 当我们有一次并发量达到了10. 以后并发量虽然下去了, 连接池中也会保持10个连接.

max_overflow
当连接池里的连接数已达到, pool_size时, 且都被使用时. 又要求从连接池里获取连接时, max_overflow就是允许再新建的连接数.
例如pool_size=10, max_overflow=5. 当我们的并发量达到12时, 当第11个并发到来后, 就会去再建一个连接, 第12个同样. 当第11个连接处理完回收后, 若没有在等待进程获取连接, 这个连接将会被立即释放.

pool_timeout
从连接池里获取连接, 如果此时无空闲的连接. 且连接数已经到达了pool_size+max_overflow. 此时获取连接的进程会等待pool_timeout秒. 如果超过这个时间, 还没有获得将会抛出异常.
sqlalchemy默认30秒

pool_recycle
这个指, 一个数据库连接的生存时间. 例如pool_recycle=3600. 也就是当这个连接产生1小时后, 再获得这个连接时, 会丢弃这个连接, 重新创建一个新的连接.
当pool_recycle设置为-1时, 也就是连接池不会主动丢弃这个连接. 永久可用. 但是有可能数据库server设置了连接超时时间. 例如mysql, 设置的有wait_timeout默认为28800, 8小时. 当连接空闲8小时时会自动断开. 8小时后再用这个连接也会被重置.
"""
engine = create_async_engine(
    settings.DATABASE_URL,  # postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}
    echo=False,  # 是否打印出实际执行的 sql, 调试的时候可能更方便
    future=True,  # 使用 SQLAlchemy 2.0 API, 向后兼容
    max_overflow=10,  # 当连接池里的连接数已达到 pool_size 且都被使用时,
    pool_size=5,  # 接池中保持的连接数, 设置为 0 时表示连接无限制
    pool_recycle=60 * 20,  # 20 minutes, 设置时间以限制数据库自动断开
    pool_timeout=30.0,  # 如果超过这个时间, 还没有获得将会抛出异常
)
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # session.commit 之后仍然可以查询该对象
)
