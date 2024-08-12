# app/crud.py

from app.db import engine, Base
from app.data.schemas.email import Email

def init_db():
    Base.metadata.create_all(bind=engine)
