from datasource.pg_session import Base
from sqlalchemy import Column, Integer, String


class RandomTable(Base):
    __tablename__ = "RANDOM_TABLE"

    id = Column(Integer, primary_key=True)
    name = Column(String)
