"""生产环境下 gunicorn 的配置文件"""

from multiprocessing import cpu_count
from os import getcwd, path

from dotenv import load_dotenv

for env_file in (".env", ".env.production"):
    env = path.join(getcwd(), env_file)
    if path.exists(env):
        load_dotenv(env)


preload_app = True  # 预加载资源, 通过预加载应用程序, 你可以节省RAM资源, 并且加快服务器启动时间
reload = True  # 程序文件修改后自动重载
bind = "127.0.0.1:8000"
# backlog = 512  # 监听队列, 等待队列最大长度,超过这个长度的链接将被拒绝连接
backlog = 2048  # 监听队列, 等待队列最大长度,超过这个长度的链接将被拒绝连接
timeout = 600  # 秒
loglevel = "info"
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 日志记录格式
accesslog = "-"  # 默认路径记录日志
errorlog = "-"
# daemon = True  # 开启后台运行
worker_class = "uvicorn.workers.UvicornWorker"
workers = cpu_count() * 2 + 1  # socketio 只能开 1 个 worker
threads = cpu_count() * 2  # 线程数 cup数量 * 2
worker_connections = 1200
