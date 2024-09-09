from pydantic import BaseModel, Field, EmailStr
from typing import Any, Dict, Optional
from datetime import datetime

class ContactModel(BaseModel):
    name:Optional[str] = None 
    email: Optional[EmailStr] = None
    date: Optional[datetime] = None
    message_id: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name":"Abc",
                "From": "example@domain.com",
                "Date": "2024-08-14T13:42:00",
                "Message-ID": "<CAMKGE15Hd8xQTo34rJCS6JzDYZhjv21UWcOXmv8XT68CHqXWrA@mail.gmail.com>",
            }
        }
