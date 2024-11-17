from colorama import Fore, init
from fastapi import status

init()
"""
框架异常类
"""


class AuthenticationError(Exception):
    """
    未认证
    """

    __slots__ = ["message"]

    def __init__(
        self, message: str = "Unauthorized", status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(
            Fore.RED + message
        )  # Add color to exception message, RED, MAGENTA, CYAN, YELLOW
        self.message = message
        self.status_code = status_code


class AuthorizationError(Exception):
    """
    未授权
    """

    __slots__ = ["message"]

    def __init__(self, message: str = "Forbidden", status_code: int = status.HTTP_403_FORBIDDEN):
        super().__init__(
            Fore.RED + message
        )  # Add color to exception message, RED, MAGENTA, CYAN, YELLOW
        self.message = message
        self.status_code = status_code
