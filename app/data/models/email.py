from pydantic import BaseModel, Field, EmailStr
from typing import Any, Dict, Optional
from datetime import datetime

class EmailModel(BaseModel):
    from_: Optional[EmailStr] = None
    to: Optional[EmailStr] = None
    date: Optional[datetime] = None
    message_id: Optional[str] = None
    subject: Optional[str] = None
    content_type: Optional[str] = None
    body: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "From": "example@domain.com",
                "To": "recipient@domain.com",
                "Date": "2024-08-14T13:42:00",
                "Message-ID": "<CAMKGE15Hd8xQTo34rJCS6JzDYZhjv21UWcOXmv8XT68CHqXWrA@mail.gmail.com>",
                "Subject": "Hello World",
                "Content-Type": "text/html; charset=UTF-8",
                "body": "This is the body of the email",
                "metadata": {"key": "value"}
            }
        }
