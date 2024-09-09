from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, Dict
import json

from ...database.db import Base

class Authroity(Base):
    __tablename__ = "authority"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    subject = Column(String, index=True, nullable=True)
    from_ = Column(String, nullable=True) 
    to = Column(String, nullable=True)  
    date = Column(DateTime, nullable=True)
    message_id = Column(String, unique=True, index=True, nullable=True)  
    body = Column(Text, nullable=True) 
    content_type = Column(String, nullable=True) 
    metaData = Column(Text, nullable=True)
    email_type = Column(Text , nullable = True)
    def set_metadata(self, data):
        self.metaData = json.dumps(data)

    def get_metadata(self):
        return json.loads(self.metaData) if self.metaData else {}