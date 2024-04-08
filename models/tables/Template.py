from datasource.pg_session import Base
from sqlalchemy import Column, Integer, String, ForeignKey
import bcrypt


class Template(Base):
    __tablename__ = "TEMPLATES"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True, nullable=True)
