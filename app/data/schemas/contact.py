
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, Dict
import json

from ...database.db import Base

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, nullable=True , unique=True,)
    date = Column(DateTime, nullable=True)  
    message_id = Column(String,index=True, nullable=True) 
    def set_metadata(self, data):
        self.metaData = json.dumps(data)
    def get_metadata(self):
        return json.loads(self.metaData) if self.metaData else {}

