from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datasource.pg_session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth.user_auth import authenticate_user, create_access_token


router = APIRouter()


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
