from fastapi import APIRouter, HTTPException
from models.validators.user import UserModel
from models.tables.User import User
from datasource.pg_session import db_dependency

router = APIRouter()


@router.get("/read/")
async def get_users(db: db_dependency):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create/")
async def create_user(user: UserModel, db: db_dependency):
    try:
        db_user = User(username=user.username, name=user.name)
        db.add(db_user)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user
