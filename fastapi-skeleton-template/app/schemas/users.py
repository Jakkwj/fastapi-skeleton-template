from pydantic import BaseModel


class SignToken(BaseModel):
    sign: str


class Token(SignToken):
    token_type: str
    access_token: str
    refresh_token: str
    sign: str


class User(BaseModel):
    username: str
    password: str


class UserSignUp(User):
    email: str
    sign: str
