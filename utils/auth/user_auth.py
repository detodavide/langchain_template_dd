from fastapi.security import OAuth2PasswordBearer
from models.tables import User
from sqlalchemy.orm import Session
import jwt
import bcrypt
import datetime
from fastapi import Depends, HTTPException, status
from datasource.pg_session import get_db
from utils.env_variables import get_env_variable

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SECRET_KEY = get_env_variable("SECRET_TOKEN_KEY")


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.checkpw(
        password.encode("utf-8"), user.hashed_password.encode("urf-8")
    ):
        return False
    return user


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algotithm="HS256")
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
