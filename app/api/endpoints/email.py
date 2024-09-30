import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc, or_

from app.data.models.customer_inbox import CustomerInboxModel
from app.data.schemas.replies import EmailReply
from ...database.db import  to_json, get_db
from ...ret_emails.read_emails import fetch_latest_email, fetch_sent_emails
from app.data.schemas.customer_inbox import CustomerInbox
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ...database.crud import create_email
import os
from ...utils.utils import serialize_email , extract_name , serialize_reply

emailRouter = APIRouter()
logging.basicConfig(level=logging.INFO)
load_dotenv()

@emailRouter.get("/emails/contact")
async def read_emails_by_contact(contact_id: int = Query(..., description="The ID of the contact to read all the emails from that contact"),db: Session = Depends(get_db)):
    print(contact_id)
    emails = db.query(CustomerInbox).order_by(desc(CustomerInbox.date)).filter(CustomerInbox.contact_id == contact_id).all()
    if not emails:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No emails found for contact {contact_id}")
    serialized_emails = [serialize_email(email) for email in emails]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"emails":serialized_emails}
    )


@emailRouter.get("/store-email", response_model=None)
async def store_emails(db: Session = Depends(get_db)):
    imap_server = os.getenv("IMAP_SERVER")
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    all_mailbox_emails = []
    inbox_email = fetch_latest_email(imap_server, username, password,mailbox="INBOX")

    sent_email = []
    #fetch_sent_emails(imap_server, username, password)
    all_mailbox_emails.append(inbox_email)

    print("SENT EMAIL " , len(sent_email))
    all_mailbox_emails.append(sent_email)
    print("Length" ,len(sent_email))
    try:
        if all_mailbox_emails:
            for mail_box in all_mailbox_emails:
                for email in mail_box:
                    create_email(email , db=db)
                return JSONResponse(
                        status_code=status.HTTP_201_CREATED,
                        content={"msg":f"Successfully stored emails , storedLength {len(all_mailbox_emails)}"}
                    )
        else:
            print("No email found or an error occurred.")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"msg": "Unable To Store Emails"}
        )
    finally:
        db.close()


@emailRouter.get("/emails/", response_model=list[CustomerInboxModel] )
def read_emails(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    emails =  db.query(CustomerInbox).order_by(desc(CustomerInbox.date)).offset(skip).limit(limit).all()
    serialized_emails = [serialize_email(email) for email in emails]
    # return emails
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"emails":serialized_emails}
    )


@emailRouter.get("/emails/{sender_email}", response_model=list[CustomerInboxModel] )
def read_specific_email(sender_email: str , skip: int = 0, limit: int = 10 ,db: Session = Depends(get_db)):
    emails = db.query(CustomerInbox).order_by(desc(CustomerInbox.date)).filter(or_(CustomerInbox.from_ == sender_email ,CustomerInbox.to == sender_email, )).all()
    replied_emails = db.query(EmailReply).order_by(desc(EmailReply.date)).filter(CustomerInbox.from_ == sender_email).all()
    serialized_emails = [serialize_email(email) for email in emails]
    serialized_replies = [serialize_reply(email) for email in replied_emails]

    if not emails:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No emails found for sender {sender_email}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"replies":serialized_replies,
            "emails":serialized_emails}
    )

@emailRouter.delete("/emails/")
async def delete_emails(db: Session = Depends(get_db)):
    db.query(CustomerInbox).delete()
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"msg": "Successfully Deleted Emails"}
    )


