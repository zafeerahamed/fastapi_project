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
        from_attributes = True # It tells Pydantic to treat ORM models as dictionaries, allowing for easier serialization and deserialization.
        json_encoders = {
            datetime: lambda v: v.date()
        } # encodes the timestamp and returns only date.

class UserCreate(BaseModel):
    email : EmailStr # validates the email format.
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
    