# app/models.py

from sqlalchemy import Column, Integer, String
from ...database.db import Base

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    from_ = Column(String)
    body = Column(String)
    message_id = Column(String, unique=True, index=True)
