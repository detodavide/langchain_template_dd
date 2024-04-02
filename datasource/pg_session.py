from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv, find_dotenv
from fastapi import Depends
from typing import Annotated
import os
from utils.env_variables import get_env_variable, load_db_variables

load_dotenv(find_dotenv())
engine = create_engine(load_db_variables())
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
