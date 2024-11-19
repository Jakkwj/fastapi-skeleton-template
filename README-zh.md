[English](https://github.com/Jakkwj/fastapi-skeleton-template) |[简体中文](https://github.com/Jakkwj/fastapi-skeleton-template/blob/master/README-zh.md)

## 简介

- 一个开箱即用的 **FastAPI** 脚手架，在源项目 [fastapi-skeleton](https://github.com/kaxiluo/fastapi-skeleton) 的基础上进行了升级和调整，集成了以下模块：

  - 数据库

    - [postgresql](https://www.postgresql.org) + [redis](https://github.com/redis/redis)
    - `ORM`模型: [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
    - 迁移: [alembic](https://github.com/sqlalchemy/alembic)

  - `JWT`认证：提供`raccess_token` 和 `refresh_token`认证
  - 日志系统：[loguru](https://github.com/Delgan/loguru)，优雅、简洁的日志库
  - 调度任务: [funboost](https://github.com/ydf0509/funboost) ，非常牛逼的万能分布式函数调度框架
  - 异常处理：自定义认证异常类
  - 路由注册：集中注册
  - 中间件: 默认注册了全局 `CORS` 中间件
  - 系统配置：

    - 基于 `pydantic.BaseSettings`，使用 `.env` 文件设置环境变量
    - 配置文件按功能模块划分，包括基础配置、数据库配置、日志配置、邮箱配置、认证配置

---

## 运行

### 1. 安装要求

- `python`版本：`3.11+`
- `uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`

### 2. 初始化

#### 数据库

- 首先, 需要在`postgresql`数据库中新建一个`test`数据库
- 然后, 通过`alembic`新建一个`User`表
- 最后通过`update_db.py`新建一个用户

```bash
# 初始化 alembic
python -m alembic init alembic

# 修改 alembic.ini 文件
# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = postgresql+psycopg2://postgres:test@127.0.0.1:4331/test

# env.py 文件导入 Base, 这样就能通过修改 models 文件夹内的类使得数据库自动迁移
# target_metadata = None
from app.models.base_model import Base
target_metadata = Base.metadata

# 使用命令 alembic revision --autogenerate -m "备注", 生成当前的版本
python -m alembic revision --autogenerate -m "init_db"

# 使用命令alembic upgrade head将alembic的版本更新到最新版
python -m alembic upgrade head


# 通过同步引擎连接 postgresql, 新建一个 User (用户名和密码都是test)
python update_db.py
```

#### aioredis

- `aioredis 2.0.1` , `redis 7.x`时, 启动连接时会报错`TypeError: duplicate base class TimeoutError`, 需要手动修改`lib/python3.11/site-packages/aioredis `目录下的`exceptions.py`文件

```python
# 将第 14 行
class TimeoutError(asyncio.TimeoutError, builtins.TimeoutError, RedisError):
pass

# 修改为如下代码, 即可运行
class TimeoutError(asyncio.exceptions.TimeoutError, RedisError):
    pass
```

### 3. 启动

- `fastapi`与调度任务框架`funboost`是分别启动的:
  - **fastapi**
    - 开发环境：进入根目录，运行 `python main.py`或者 `fastapi dev`
    - 生成环境：通过 `supervisor`调用 `gunicorn`的配置文件 `fastapi-skeleton-template/storage/supervisor/gconfig.py`

  - **scheduler**
    - 开发环境：进入根目录，运行 `python scheduler.py`
    - 生成环境：通过 `supervisor`调用 `fastapi-skeleton-template/storage/supervisor/scheduler.py`


---

## 文件夹结构

```
/fastapi-skeleton-template/
|-- alembic
|   |   |-- versions
|   |   |   |-- 7d5554c55cbb_init_db.py         ----- alembic 数据库初始化
|   |   |-- env.py
|   |   |-- README
|   |   `-- script.py.mako
|-- app
|   |   |-- exceptions                          ----- 自定义的异常类
|   |   |    |-- __init__.py
|   |   |    `-- exception.py
|   |-- http                                    ----- http目录
|   |   |-- api                                 ----- api接口目录
|   |   |   |-- task                            ----- 任务调度目录
|   |   |   |   |-- __init__.py
|   |   |   |    `-- test.py                    ----- 任务调度接口
|   |   |   |-- user                            ----- 任务调度目录
|   |   |   |   |-- __init__.py
|   |   |   |   |-- auth.py                     ----- 登录认证接口
|   |   |   |    `-- sign.py                    ----- 用户注册接口
|   |   |   |-- __init__.py
|   |   |-- middleware                          ----- 自定义中间件
|   |   |   `-- __init__.py
|   |   |-- __init__.py
|   |   `-- deps.py                             ----- 依赖
|   |-- models                                  ----- 模型目录
|   |   |-- __init__.py
|   |   |-- base_model.py                       ----- 定义模型的基类
|   |   `-- user.py
|   |-- providers                               ----- 核心服务提供者
|   |   |-- __init__.py
|   |   |-- app_provider.py                     ----- 注册应用的全局事件、中间件等
|   |   |-- database.py                         ----- 数据库连接
|   |   |-- handle_exception.py                 ----- 异常处理器
|   |   |-- logging_provider.py                 ----- 集成loguru日志系统
|   |   `-- route_provider.py                   ----- 注册路由文件routes/*
|   |-- schemas                                 ----- 数据模型，负责请求和响应资源数据的定义和格式转换
|   |   |-- __init__.py
|   |   `-- user.py
|   |-- services                                ----- 服务层，业务逻辑层
|   |   |-- auth                                ----- 认证相关服务
|   |   |   |-- __init__.py
|   |   |   |-- grant.py                        ----- 认证核心类
|   |   |   |-- jwt_helper.py
|   |   |   `-- users.py
|   |   |-- email                               ----- 邮件相关服务
|   |   |   |-- __init__.py
|   |   |   `-- email.py
|   |   |-- crypto.py                           ----- 加密解密相关服务
|   |   |-- redis.py                            ----- redis同步服务
|   |   |-- task.py                             ----- 调度任务相关服务
|   |   `-- __init__.py
|   |-- support                                 ----- 公共方法
|   |   |-- __init__.py
|   |   `-- asyncio.py                          ----- uvloop 替换 asyncio
|   |-- tasks                                   ----- 调度任务
|   |   |-- __init__.py
|   |   |-- params.py                           ----- funboost 入参
|   |   `-- task_test.py                        ----- 调度任务主体
|-- bootstrap                                   ----- 启动项
|   |-- __init__.py
|   `-- application.py                          ----- 创建app实例
|-- config                                      ----- 配置目录
|   |-- settings                                ----- 配置子目录
|   |   |-- __init__.py
|   |   |-- dir.py                              ----- 配置路径配置
|   |   |-- email.py                            ----- 邮件配置
|   |   |-- logging.py                          ----- 日志配置
|   |   `-- redis.py                            ----- redis 配置
|   |-- __init__.py
|   `-- config.py                               ----- app配置
|-- routes                                      ----- 路由目录
|   |-- __init__.py
|   `-- api.py                                  ----- api路由
|-- static                                      ----- 静态资源目录
|   |-- fastapi
|   |    |-- swagger-ui@5.17.14                 ----- swagger
|   |    |    |-- favicon-32x32.png
|   |    |    |-- swagger-ui.css
|   |    |    |-- swagger-ui.css.map
|   |    |    `-- swagger-ui-bundle.js
|-- storage
|   |-- logs                                    ----- 日志目录
|   |-- supervisor                              -----  supervisor 配置文件
|   |   |-- fastapi.conf                        ----- fastapi 的 supervisor 配置文件
|   |   `-- scheduler.conf                      ----- scheduler 的 supervisor 配置文件
|   `-- tmp                                     ----- 临时文件
|-- .env                                        ----- 环境配置
|-- .env.development                            ----- 开发环境配置
|-- .env.production                             ----- 生产环境配置
|-- alembic.ini                                 ----- alembic 配置
|-- funboost_config.py                          ----- funboost 首次启动时自动生成配置文件
|-- gconfig.py                                  ----- 生产环境下 gunicorn 的配置文件
|-- main.py                                     ----- app/api启动入口
|-- nb_log_config.py                            ----- funboost 首次启动时自动生成的nb_log日志配置文件
|-- requirements.txt
|-- ruff.toml                                   ----- ruff 配置文件
|-- scheduler.py                                ----- funboost 调度任务启动入口
`-- update_db.py                                ----- 数据库更新脚本
```

### alembic 文件夹

- `alembic`文件夹包含了数据库迁移程序的核心代码。

### app 文件夹

- `app`文件夹包含了应用程序的核心代码
- 测试环境下, `fastapi-skeleton-template/app/services/crypto.py`中的加密解密功能都是跳过的
- `redis`
  - `fastapi`启动时, 是异步连接的` redis``
  - ``fastapi-skeleton-template/app/services/redis.py`中是同步 `redis`工具

### bootstrap 文件夹

- `bootstrap` 文件夹包含了 `application.py` 文件，该文件用于引导框架，创建 `Fastapi`实例。

### config 文件夹

- `config`文件夹目录，顾名思义，包含了应用程序的所有配置文件。

### routes 文件夹

- `routes`文件夹包含了应用程序的所有路由定义。

### static 文件夹

- `swagger-ui`在国内难以访问，需要先下载保存到本地。

- [解决 fastapi 访问/docs 和/redoc 接口文档显示空白或无法加载](https://blog.csdn.net/weixin_43936332/article/details/131020726)

- 下载[swagger-ui](https://github.com/swagger-api/swagger-ui)

- 然后我们需要在 python 解释器环境(或虚拟环境)下 Lib/site-package/fastapi/openapi/docs.py 文件修改里面的静态资源访问路径:

  ```python
  swagger_js_url = "/static/fastapi/swagger-ui@5.17.14/swagger-ui-bundle.js"
  swagger_css_url = "/static/fastapi/swagger-ui@5.17.14/swagger-ui.css"
  swagger_favicon_url = "/static/fastapi/swagger-ui@5.17.14/favicon-32x32.png"
  ```

- 然后在`fastapi-skeleton-template/bootstrap/application.py`中挂载静态资源文件夹

  ```python
  app.mount(
      "/static",
      StaticFiles(directory="static"),
      name="static",
  )
  ```

### storage 文件夹

- `storage`文件夹用于存放日志文件，临时文件及其他资料性文件
  - `logs`文件夹: 用于存放日志文件
  - ` supervisor`文件夹: 用于存放 `supervisor`的配置文件
  - `tmp`文件夹: 临时及其他资料性文件

---

## 参考

- [FastAPI 官方中文文档](https://fastapi.tiangolo.com/zh/)
- 代码结构组织风格参考 [Laravel 框架](https://github.com/laravel/laravel)
- [python 万能分布式函数调度框架简 funboost](https://github.com/ydf0509/funboost)
- [alembic](https://github.com/sqlalchemy/alembic): https://blog.csdn.net/f066314/article/details/122416386
