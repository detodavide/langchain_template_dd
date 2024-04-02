from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    name: str


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
