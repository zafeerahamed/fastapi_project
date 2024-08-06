from pydantic import BaseModel
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