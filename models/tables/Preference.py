from datasource.pg_session import Base
from sqlalchemy import Column, Integer, String, ForeignKey
import bcrypt


class Preference(Base):
    __tablename__ = "PREFERENCES"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    llm = Column(String, index=True, nullable=True)
    template_id = Column(String, index=True, nullable=True)
