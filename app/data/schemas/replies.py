
from sqlalchemy import Column, Integer, String, Text, DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, Dict
import json

from ...database.db import Base

class EmailReply(Base):
    __tablename__ = "email_replies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    subject = Column(String, index=True, nullable=True)
    from_ = Column(String, nullable=True)  # Assuming the `from_` field stores email addresses as strings
    to = Column(String, nullable=True)  # Adding `to` field
    date = Column(DateTime, nullable=True)  # Adding `date` field
    message_id = Column(String, unique=True, index=True, nullable=True)  # Ensure uniqueness
    body = Column(Text, nullable=True)  # Using Text for potentially large body content
    content_type = Column(String, nullable=True)  # Adding `content_type` field
    meta_data = Column(Text, nullable=True)  # Store metadata as JSON string
    email_type = Column(Text , nullable = True)
    parent_message_id = Column(Integer, ForeignKey('customer_inbox.message_id'), nullable=True , index=True)
    customer_inbox = relationship("CustomerInbox", back_populates="replies")
    
    def set_metadata(self, data):
        self.meta_data = json.dumps(data)

    def get_metadata(self):
        return json.loads(self.meta_data) if self.meta_data else {}