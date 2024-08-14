import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status
from ...database.db import  to_json, get_db
from ...ret_emails.read_emails import fetch_latest_email
from app.data.schemas.email import Email
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ...database.crud import create_email
import os


emailRouter = APIRouter()
logging.basicConfig(level=logging.INFO)
load_dotenv()


@emailRouter.get("/store-email", response_model=None)
async def store_emails(db: Session = Depends(get_db)):
    imap_server = os.getenv("IMAP_SERVER")
    username = "testmail@migrando.de"
    password = "KxBHfJksz8T5wU5dULxN"
    latest_email = fetch_latest_email(imap_server, username, password)
    try:
        if latest_email:
            for email in latest_email:
                create_email(subject=email["subject"], body=email["body"],
                             from_=email["from"], message_id=email["message_id"] , db=db)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"msg": "Successfully Stored Emails"}
            )
        else:
            print("No email found or an error occurred.")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"msg": "Unable To Store Emails"}
        )
    finally:
        db.close()


@emailRouter.get("/emails/")
def read_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    emails = db.query(Email).offset(skip).limit(limit).all()
    return emails
    # return JSONResponse(
    #     status_code=status.HTTP_200_OK,
    #     content=emails
    # )


@emailRouter.delete("/emails/")
async def delete_emails(db: Session = Depends(get_db)):
    db.query(Email).delete()
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"msg": "Successfully Deleted Emails"}
    )
