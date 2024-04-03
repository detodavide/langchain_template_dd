from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserModel(BaseModel):
    username: str
    name: str


class UserIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    password: str


class UserOut(BaseModel):
    username: str
