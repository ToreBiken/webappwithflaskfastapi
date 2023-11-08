from pydantic import BaseModel

class UserBase(BaseModel):
    login: str
    email: str
    
class WorkBase(BaseModel):
    work_title: str
    work_description: str
    
class WorkCreate(WorkBase):
    work_owner: int

class Work(WorkBase):
    work_id: int
    work_owner: int
    
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    user_id: int
    user_works: list[Work] = []
    
    class Config:
        orm_mode = True