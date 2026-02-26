from sqlalchemy import Column, Interger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Interger, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Interger, ForeignKey("roles.id"))
    role = relationship("Role")
    tasks = relationship("Task", back_populates="owner")
