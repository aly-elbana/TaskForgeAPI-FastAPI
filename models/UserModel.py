from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from utils.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")