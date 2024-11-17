[English](https://github.com/Jakkwj/fastapi-skeleton-template) |[简体中文](https://github.com/Jakkwj/fastapi-skeleton-template/blob/master/README-zh.md)

## Introduction

- A ready-to-use **FastAPI** skeleton, upgraded and adjusted based on the source project [fastapi-skeleton](https://github.com/kaxiluo/fastapi-skeleton), integrating the following modules:

  - Database

    - [postgresql](https://www.postgresql.org) + [redis](https://github.com/redis/redis)
    - `ORM` model: [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
    - Migration: [alembic](https://github.com/sqlalchemy/alembic)

  - `JWT` authentication: Providing `access_token` and `refresh_token` authentication
  - Logging system: [loguru](https://github.com/Delgan/loguru), an elegant and concise logging library
  - Scheduling tasks: [funboost](https://github.com/ydf0509/funboost), a very powerful universal distributed function scheduling framework
  - Exception handling: Custom authentication exception classes
  - Route registration: Centralized registration
  - Middleware: Default registration of global `CORS` middleware
  - System configuration:

    - Based on `pydantic.BaseSettings`, using `.env` file to set environment variables
    - Configuration files are divided according to functional modules, including basic configuration, database configuration, logging configuration, email configuration, and authentication configuration

---

## Running

### 1. Installation Requirements

- `python`version：`3.11+`
- `uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`

### 2. Initialization

#### database

- [alembic](https://github.com/sqlalchemy/alembic): https://blog.csdn.net/f066314/article/details/122416386

```bash
# Install alembic
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt
python -m alembic init alembic

# Modify alembic.ini file
# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = postgresql+psycopg2://postgres:test@127.0.0.1:4331/sludge_web

# env.py file imports Base, so that database migrations can be automatically made by modifying classes within the models folder
# target_metadata = None
from app.models.base_model import Base
target_metadata = Base.metadata

# Use the command alembic revision --autogenerate -m "note" to generate the current version
python -m alembic revision --autogenerate -m "init_db"

# Use the command alembic upgrade head to update alembic to the latest version
python -m alembic upgrade head

# Initialize the database
python update_db.py
```

#### aioredis

- When using `python 3.11`, `aioredis 2.0.1`, `redis 7.x`, an error `TypeError: duplicate base class TimeoutError` will occur when starting the connection. Locate to line 14 in the `exceptions.py` file under the `aioredis` directory

```python
class TimeoutError(asyncio.TimeoutError, builtins.TimeoutError, RedisError):
pass

# Modify the code as follows to run
class TimeoutError(asyncio.exceptions.TimeoutError, RedisError):
    pass
```

### 3. Startup

- `fastapi` and the scheduling task framework are started separately
- **fastapi**
  - Development environment: Enter the root directory and run `python main.py` or `fastapi dev`
  - Production environment: Call `gunicorn` configuration file `fastapi-skeleton-template/storage/supervisor/gconfig.py` through `supervisor`
- **scheduler**
  - Development environment: Enter the root directory and run `python scheduler.py`
  - Production environment: Call `fastapi-skeleton-template/storage/supervisor/scheduler.py` through `supervisor`

---

## Folder Structure

```
/fastapi-skeleton-template/
|-- alembic
|   |   |-- versions
|   |   |   |-- 7d5554c55cbb_init_db.py         ----- alembic database initialization
|   |   |-- env.py
|   |   |-- README
|   |   `-- script.py.mako
|-- app
|   |   |-- exceptions                          ----- Custom exception classes
|   |   |    |-- __init__.py
|   |   |    `-- exception.py
|   |-- http                                    ----- http directory
|   |   |-- api                                 ----- api interface directory
|   |   |   |-- task                            ----- Task scheduling directory
|   |   |   |   |-- __init__.py
|   |   |   |    `-- test.py                    ----- Task scheduling interface
|   |   |   |-- user                            ----- Task scheduling directory
|   |   |   |   |-- __init__.py
|   |   |   |   |-- auth.py                     ----- Login authentication interface
|   |   |   |    `-- sign.py                    ----- User registration interface
|   |   |   |-- __init__.py
|   |   |-- middleware                          ----- Custom middleware
|   |   |   `-- __init__.py
|   |   |-- __init__.py
|   |   `-- deps.py                             ----- Dependencies
|   |-- models                                  ----- Model directory
|   |   |-- __init__.py
|   |   |-- base_model.py                       ----- Define the base class of models
|   |   `-- user.py
|   |-- providers                               ----- Core service providers
|   |   |-- __init__.py
|   |   |-- app_provider.py                     ----- Register application's global events, middleware, etc.
|   |   |-- database.py                         ----- Database connection
|   |   |-- handle_exception.py                 ----- Exception handler
|   |   |-- logging_provider.py                 ----- Integrate loguru logging system
|   |   `-- route_provider.py                   ----- Register route files routes/*
|   |-- schemas                                 ----- Data models, responsible for the definition and format conversion of request and response resource data
|   |   |-- __init__.py
|   |   `-- user.py
|   |-- services                                ----- Service layer, business logic layer
|   |   |-- auth                                ----- Authentication-related services
|   |   |   |-- __init__.py
|   |   |   |-- grant.py                        ----- Authentication core class
|   |   |   |-- jwt_helper.py
|   |   |   `-- users.py
|   |   |-- email                               ----- Email-related services
|   |   |   |-- __init__.py
|   |   |   `-- email.py
|   |   |-- crypto.py                           ----- Encryption and decryption-related services
|   |   |-- redis.py                            ----- Synchronous redis service
|   |   |-- task.py                             ----- Scheduling task-related services
|   |   `-- __init__.py
|   |-- support                                 ----- Public methods
|   |   |-- __init__.py
|   |   `-- asyncio.py                          ----- uvloop replaces asyncio
|   |-- tasks                                   ----- Scheduling tasks
|   |   |-- __init__.py
|   |   |-- params.py                           ----- funboost input parameters
|   |   `-- task_test.py                        ----- Main body of scheduling tasks
|-- bootstrap                                   ----- Startup items
|   |-- __init__.py
|   `-- application.py                          ----- Create Fastapi instance
|-- config                                      ----- Configuration directory
|   |-- settings                                ----- Configuration subdirectory
|   |   |-- __init__.py
|   |   |-- dir.py                              ----- Configuration path configuration
|   |   |-- email.py                            ----- Email configuration
|   |   |-- logging.py                          ----- Logging configuration
|   |   `-- redis.py                            ----- Redis configuration
|   |-- __init__.py
|   `-- config.py                               ----- App configuration
|-- routes                                      ----- Route directory
|   |-- __init__.py
|   `-- api.py                                  ----- Api routes
|-- static                                      ----- Static resource directory
|   |-- fastapi
|   |    |-- swagger-ui@5.17.14                 ----- swagger
|   |    |    |-- favicon-32x32.png
|   |    |    |-- swagger-ui.css
|   |    |    |-- swagger-ui.css.map
|   |    |    `-- swagger-ui-bundle.js
|-- storage
|   |-- logs                                    ----- Log directory
|   |-- supervisor                              ----- Supervisor configuration files
|   |   |-- fastapi.conf                        ----- Supervisor configuration file for fastapi
|   |   `-- scheduler.conf                      ----- Supervisor configuration file for scheduler
|   `-- tmp                                     ----- Temporary files
|-- .env                                        ----- Environment configuration
|-- .env.development                            ----- Development environment configuration
|-- .env.production                             ----- Production environment configuration
|-- alembic.ini                                 ----- Alembic configuration
|-- funboost_config.py                          ----- Funboost automatically generates a configuration file upon first startup
|-- gconfig.py                                  ----- Gunicorn configuration file for production environment
|-- main.py                                     ----- App/api startup entry
|-- nb_log_config.py                            ----- Funboost automatically generates nb_log logging configuration file upon first startup
|-- requirements.txt
|-- ruff.toml                                   ----- Ruff configuration file
|-- scheduler.py                                ----- Funboost scheduling task startup entry
`-- update_db.py                                ----- Database update script
```

### alembic Folder

- The `alembic` folder contains the core code of the database migration program

### app Folder

- The `app` folder contains the core code of the application
- In the test environment, the encryption and decryption functions in `fastapi-skeleton-template/app/services/crypto.py` are skipped
- `redis`
  - When `fastapi` starts, it connects to `redis` asynchronously
  - `fastapi-skeleton-template/app/services/redis.py` contains synchronous `redis` utilities

### bootstrap Folder

- The `bootstrap` folder contains the `application.py` file, which is used to bootstrap the framework and create a `Fastapi` instance

### config Folder

- The `config` folder, as the name suggests, contains all the configuration files of the application

### routes Folder

- The `routes` folder contains all the route definitions of the application

### static Folder

- `swagger-ui` is difficult to access in China, so it needs to be downloaded and saved locally

- [Solving the problem of fastapi accessing /docs and /redoc interface documentation showing blank or unable to load](https://blog.csdn.net/weixin_43936332/article/details/131020726)

- Download [swagger-ui](https://github.com/swagger-api/swagger-ui)

- Then we need to modify the static resource access path in the Lib/site-package/fastapi/openapi/docs.py file under the Python interpreter environment (or virtual environment):

  ```python
  swagger_js_url = "/static/fastapi/swagger-ui@5.17.14/swagger-ui-bundle.js"
  swagger_css_url = "/static/fastapi/swagger-ui@5.17.14/swagger-ui.css"
  swagger_favicon_url = "/static/fastapi/swagger-ui@5.17.14/favicon-32x32.png"
  ```

- Then mount the static resource folder in `fastapi-skeleton-template/bootstrap/application.py`

  ```python
  app.mount(
      "/static",
      StaticFiles(directory="static"),
      name="static",
  )
  ```

### storage Folder

- The `storage` folder is used to store log files, temporary files, and other material files
  - `logs` folder: Used for storing log files
  - `supervisor` folder: Used for storing the configuration files for `supervisor`
  - `tmp` folder: Used for temporary and other reference files

---

## References

- [FastAPI Official Chinese Documentation](https://fastapi.tiangolo.com/zh/)
- Code structure organization style refers to [Laravel Framework](https://github.com/laravel/laravel)
- [Python Universal Distributed Function Scheduling Framework Simple Funboost](https://github.com/ydf0509/funboost)
