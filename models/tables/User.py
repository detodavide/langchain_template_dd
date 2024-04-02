from datasource.pg_session import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "USER"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    name = Column(String, index=True, nullable=True)
