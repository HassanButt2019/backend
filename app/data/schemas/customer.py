
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, Dict
import json

from ...database.db import Base

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, nullable=True, unique=True)
    date = Column(DateTime, nullable=True)  
    application_number = Column(String, nullable=True)
    email_count = Column(Integer, default=0) 
    emails = relationship("CustomerInbox", back_populates="contact") #change name of this to customer_inbox

