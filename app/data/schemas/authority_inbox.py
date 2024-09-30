from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, Dict
import json

from ...database.db import Base

class AuthroityInbox(Base):
    __tablename__ = "authority_inbox"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    subject = Column(String, index=True, nullable=True)
    from_ = Column(String, nullable=True) 
    to = Column(String, nullable=True)  
    date = Column(DateTime, nullable=True)
    message_id = Column(String, unique=True, index=True, nullable=True)  
    body = Column(Text, nullable=True) 
    content_type = Column(String, nullable=True) 
    meta_data = Column(Text, nullable=True)
    email_type = Column(Text , nullable = True)
    def set_metadata(self, data):
        self.meta_data = json.dumps(data)

    def get_metadata(self):
        return json.loads(self.meta_data) if self.meta_data else {}