import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app.data.models.email import EmailModel
from ...database.db import  to_json, get_db
from ...ret_emails.read_emails import fetch_latest_email
from app.data.schemas.email import Email
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ...database.crud import create_email
import os
from ...utils.utils import serialize_email

emailRouter = APIRouter()
logging.basicConfig(level=logging.INFO)
load_dotenv()


@emailRouter.get("/store-email", response_model=None)
async def store_emails(db: Session = Depends(get_db)):
    imap_server = os.getenv("IMAP_SERVER")
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    latest_email = fetch_latest_email(imap_server, username, password)
    try:
        if latest_email:
            for email in latest_email:
                create_email(email , db=db)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"msg":f"Successfully stored emails , storedLength {len(latest_email)}"}
            )
        else:
            print("No email found or an error occurred.")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"msg": "Unable To Store Emails"}
        )
    finally:
        db.close()


@emailRouter.get("/emails/", response_model=list[EmailModel] )
def read_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    emails = db.query(Email).offset(skip).limit(limit).all()
    serialized_emails = [serialize_email(email) for email in emails]
    # return emails
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"emails":serialized_emails}
    )

@emailRouter.get("/emails/{sender_email}", response_model=list[EmailModel] )
def read_specific_email(sender_email: str , skip: int = 0, limit: int = 10 ,db: Session = Depends(get_db)):
    emails = db.query(Email).filter(Email.from_ == sender_email).all()
    serialized_emails = [serialize_email(email) for email in emails]
    if not emails:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No emails found for sender {sender_email}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"emails":serialized_emails}
    )

@emailRouter.delete("/emails/")
async def delete_emails(db: Session = Depends(get_db)):
    db.query(Email).delete()
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"msg": "Successfully Deleted Emails"}
    )
