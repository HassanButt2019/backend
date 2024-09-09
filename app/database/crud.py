# app/crud.py

from .db import engine, Base
from app.data.schemas.email import Email
from app.data.models.email import EmailModel
from fastapi import Depends
from .db import get_db
from sqlalchemy.orm import Session
from ..data.models.authority import authorityList , AuthroityModel
from app.data.schemas.authority import Authroity
from app.data.schemas.contact import Contact


def init_db():
    Base.metadata.create_all(bind=engine)



def create_email(email: EmailModel,db: Session = Depends(get_db)):
    existing_email = db.query(Email).filter(Email.message_id == email.message_id).first()
    existing_authority_email = db.query(Authroity).filter(Authroity.message_id == email.message_id).first()
    if existing_email or existing_authority_email:
        return
    if email.from_ in authorityList:
            db_email = Authroity(
        name = email.name,
        subject=email.subject,
        from_=email.from_,
        to=email.to,
        date=email.date,
        message_id=email.message_id,
        body=email.body,
        content_type=email.content_type,
        email_type = email.email_type
            )
            db_email.set_metadata(email.metadata or {})
            db.add(db_email)
            db.commit()
            db.refresh(db_email)
            print(f"Saved email with Message-ID {email.from_} to the database. Authority")
    else:
        create_contact(name=email.name ,from_=email.from_ ,message_id= email.message_id ,date= email.date , db=db)
        db_email = Email(
        name = email.name,
        subject=email.subject,
        from_=email.from_,
        to=email.to,
        date=email.date,
        message_id=email.message_id,
        body=email.body,
        content_type=email.content_type,
        email_type = email.email_type
    )
        db_email.set_metadata(email.metadata or {})
        db.add(db_email)
        db.commit()
        db.refresh(db_email)
        print(f"Saved email with Message-ID {email.from_} to the database. Contact")




def create_contact(name:str , from_:str , message_id:str , date:str ,db: Session = Depends(get_db)):
        existing_email = db.query(Contact).filter(Contact.email == from_).first()
        if existing_email :
            return
        db_contact = Contact(
        name = name,
        email=from_,
        date=date,
        message_id=message_id,
            )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        print(f"Saved contact with Message-ID {from_} to the database. Contact")