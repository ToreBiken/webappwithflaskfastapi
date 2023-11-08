from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# import sys
# module_directory = 'D:\\projects\\fastapi_crud'
# sys.path.append(module_directory)
# import database
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    
    user_works = relationship("Work", back_populates='owner', cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, login={self.login!r}, email={self.email!r})"
    
class Work(Base):
    __tablename__ = "works"
    work_id = Column(Integer, primary_key=True)
    work_title = Column(String(255), nullable=False)
    work_description = Column(String(255), nullable=False)
    work_owner = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    owner = relationship("User", back_populates="user_works")
    
    def __repr__(self) -> str:
        return f"Work(work_id={self.work_id!r}, title={self.work_title!r}, description={self.work_description!r}, owner={self.work_owner!r})"
        