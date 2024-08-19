# app/crud.py

from .db import engine, Base
from app.data.schemas.email import Email
from app.data.models.email import EmailModel
from fastapi import Depends
from .db import get_db
from sqlalchemy.orm import Session

def init_db():
    Base.metadata.create_all(bind=engine)



def create_email(email: EmailModel,db: Session = Depends(get_db)):
    existing_email = db.query(Email).filter(Email.message_id == email.message_id).first()
    if existing_email:
        # print(f"Email with Message-ID {email.message_id} already exists. Skipping.")
        return
    db_email = Email(
        subject=email.subject,
        from_=email.from_,
        to=email.to,
        date=email.date,
        message_id=email.message_id,
        body=email.body,
        content_type=email.content_type,
    )
    db_email.set_metadata(email.metadata or {})
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    print(f"Saved email with Message-ID {email.message_id} to the database.")
