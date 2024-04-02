from datasource.pg_session import Base
from sqlalchemy import Column, Integer, String
import bcrypt


class User(Base):
    __tablename__ = "USERS"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    name = Column(String, index=True, nullable=True)
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return bcrypt.checkpw(
            password.encode("urf-8"), self.hashed_password.encode("urf-8")
        )
