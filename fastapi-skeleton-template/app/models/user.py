from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.services.auth.jwt_helper import create_token_from_user

from .base_model import Base, TimeCreated


class User(Base, TimeCreated):
    __tablename__ = "user"

    id = Column(Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(256), unique=True, nullable=False, index=True)
    email = Column(String(256), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)  # 用户是否确认账号

    @property
    def password(self):
        raise AttributeError("User's password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)  # type: ignore

    def create_token(self, expiration: int = 7200):
        return create_token_from_user(self.id, expiration)  # type: ignore
