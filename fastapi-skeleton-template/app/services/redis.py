from redis import StrictRedis

from config.config import get_settings

settings = get_settings()


class Redis:
    """
    同步 redis 数据库操作.
    有时候有些同步函数不方便用 aioredis, 则需要使用同步 redis.
    """

    @staticmethod
    def _connect():
        """连接数据库"""
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        db = settings.REDIS_DB
        return StrictRedis(host, port, db)

    @classmethod
    def write(cls, key, value, expire=None):
        """写入键值对"""
        expire_in_seconds = (
            expire if expire else settings.REDIS_EXPIRE
        )  # 判断是否有过期时间, 没有就设置默认值
        rds = cls._connect()
        rds.set(key, value, ex=expire_in_seconds)

    @classmethod
    def read(cls, key):
        """读取键值对内容"""
        rds = cls._connect()
        value = rds.get(key)
        return value.decode("utf-8") if value else value

    @classmethod
    def hset(cls, name, key, value):
        """写入 hash 表"""
        rds = cls._connect()
        rds.hset(name, key, value)

    @classmethod
    def hmset(cls, key, *value):
        """读取指定 hash 表的所有给定字段的值"""
        rds = cls._connect()
        value = rds.hmset(key, *value)
        return value

    @classmethod
    def hget(cls, name, key):
        """读取指定 hash 表的键值"""
        rds = cls._connect()
        value = rds.hget(name, key)
        return value.decode("utf-8") if value else value

    @classmethod
    def hgetall(cls, name):
        """获取指定 hash 表所有的值"""
        rds = cls._connect()
        return rds.hgetall(name)

    @classmethod
    def delete(cls, *names):
        """删除一个或者多个"""
        rds = cls._connect()
        rds.delete(*names)

    @classmethod
    def hdel(cls, name, key):
        """删除指定 hash 表的键值"""
        rds = cls._connect()
        rds.hdel(name, key)

    @classmethod
    def expire(cls, name, expire: int | None = None):
        """设置过期时间.
        注意, 过期时间只可设置在顶级 key, 而不能给 hash 的某 key 单独设置
        """
        if expire:
            expire_in_seconds: int = expire
        else:
            expire_in_seconds = settings.REDIS_EXPIRE  # 默认 60s
        rds = cls._connect()
        rds.expire(name, expire_in_seconds)
