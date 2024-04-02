from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    name: str
