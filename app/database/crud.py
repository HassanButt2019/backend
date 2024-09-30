# app/crud.py

from app.data.models.email_reply import EmailReplyModel
from app.data.schemas.replies import EmailReply
from .db import engine, Base
from app.data.schemas.customer_inbox import CustomerInbox
from app.data.models.customer_inbox import CustomerInboxModel
from fastapi import Depends
from .db import get_db
from sqlalchemy.orm import Session
from ..data.models.authority_inbox import authorityList , AuthroityInboxModel
from app.data.schemas.authority_inbox import AuthroityInbox
from app.data.schemas.customer import Customer


def init_db():
    Base.metadata.create_all(bind=engine)



def create_email(email: CustomerInboxModel,db: Session = Depends(get_db)):
    existing_email = db.query(CustomerInbox).filter(CustomerInbox.message_id == email.message_id).first()
    existing_authority_email = db.query(AuthroityInbox).filter(AuthroityInbox.message_id == email.message_id).first()
    if existing_email or existing_authority_email:
        return
    

    if "In-Reply-To" in email.metadata:
          current_reply = EmailReplyModel(
        name = email.name,
        subject=email.subject,
        from_=email.from_,
        to=email.to,
        date=email.date,
        message_id=email.message_id,
        body=email.body,
        content_type=email.content_type,
        email_type = email.email_type,
        metadata= email.metadata,
        parent_message_id= email.metadata["References"]
          )
          create_reply(
          reply=current_reply,
          db=db 
          )
    elif email.from_ in authorityList:
            db_email = AuthroityInbox(
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
        contact_Id =  create_contact(name=email.name ,from_=email.from_ ,message_id= email.message_id ,date= email.date , db=db)
        db_email = CustomerInbox(
        name = email.name,
        subject=email.subject,
        from_=email.from_,
        to=email.to,
        date=email.date,
        message_id=email.message_id,
        body=email.body,
        content_type=email.content_type,
        email_type = email.email_type,
        contact_id = contact_Id
    )
        db_email.set_metadata(email.metadata or {})
        db.add(db_email)
        db.commit()
        db.refresh(db_email)
        print(f"Saved email with Message-ID {email.from_} to the database. Contact")




def create_contact(name:str , from_:str , message_id:str , date:str ,db: Session = Depends(get_db)):
        existing_email = db.query(Customer).filter(Customer.email == from_).first()
        if existing_email :
            return existing_email.id
        db_contact = Customer(
        name = name,
        email=from_,
        date=date,
        email_count = 0 ,
        application_number = "0"
            )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        print(f"Saved contact with Message-ID {from_} to the database. Contact")
        return db_contact.id





def create_reply(reply: EmailReplyModel,db: Session = Depends(get_db)):
        existing_email = db.query(EmailReply).filter(EmailReply.message_id == reply.message_id).first()

        if existing_email :
              return
        db_email = EmailReply(
        name = reply.name,
        subject=reply.subject,
        from_=reply.from_,
        to=reply.to,
        date=reply.date,
        message_id=reply.message_id,
        body=reply.body,
        content_type=reply.content_type,
        email_type = reply.email_type,
        parent_message_id = reply.parent_message_id
    )
        db_email.set_metadata(reply.metadata or {})
        db.add(db_email)
        db.commit()
        db.refresh(db_email)
        print(f"Saved email with Message-ID {reply.from_} to the database. Contact")