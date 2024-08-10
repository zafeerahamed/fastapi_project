from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    title: str
    content: str
    created_on: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.date()
        }

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_on : datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.date()
        }
    