# app/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, Dict
import json

from ...database.db import Base

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True, nullable=True)
    from_ = Column(String, nullable=True)  # Assuming the `from_` field stores email addresses as strings
    to = Column(String, nullable=True)  # Adding `to` field
    date = Column(DateTime, nullable=True)  # Adding `date` field
    message_id = Column(String, unique=True, index=True, nullable=True)  # Ensure uniqueness
    body = Column(Text, nullable=True)  # Using Text for potentially large body content
    content_type = Column(String, nullable=True)  # Adding `content_type` field
    metaData = Column(Text, nullable=True)  # Store metadata as JSON string
    def set_metadata(self, data):
        self.metaData = json.dumps(data)

    def get_metadata(self):
        return json.loads(self.metaData) if self.metaData else {}

