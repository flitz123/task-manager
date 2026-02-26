from sqlalchemy import Column, Interger, String
from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Interger, primary_key=True)
    name = Column(String, unique=True)
