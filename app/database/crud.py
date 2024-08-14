# app/crud.py

from .db import engine, Base
from app.data.schemas.email import Email
from fastapi import Depends
from .db import get_db
from sqlalchemy.orm import Session

def init_db():
    Base.metadata.create_all(bind=engine)



def create_email(subject: str, body: str, from_: str, message_id: str,db: Session = Depends(get_db)):
    existing_email = db.query(Email).filter(Email.message_id == message_id).first()
    if existing_email:
        # print(f"Email with Message-ID {message_id} already exists. Skipping.")
        return
    db_email = Email(subject=subject, body=body, from_=from_, message_id=message_id)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    print(f"Saved email with Message-ID {message_id} to the database.")