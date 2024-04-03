from fastapi import APIRouter, HTTPException, Depends
import bcrypt
from models.validators.user import UserModel, UserIn, UserOut
from models.tables.User import User
from sqlalchemy.orm import Session
from datasource.pg_session import db_dependency

router = APIRouter()


@router.get("/read")
async def get_users(db: db_dependency):
    users = db.query(User).all()
    return users


@router.post("/create")
async def create_user(user_in: UserIn, db: db_dependency):
    db_user = db.query(User).filter(User.username == user_in.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = bcrypt.hashpw(user_in.password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(
        username=user_in.username, hashed_password=hashed_password.decode("utf-8")
    )
    db.add(new_user)
    db.commit()
    return UserOut(username=new_user.username)
