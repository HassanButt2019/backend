import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, desc

from app.data.models.authority_inbox import AuthroityInboxModel
from ...database.db import  to_json, get_db
from ...ret_emails.read_emails import fetch_latest_email
from app.data.schemas.authority_inbox import AuthroityInbox
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ...database.crud import create_email
import os
from ...utils.utils import serialize_email, serialize_email_authority

authorityRouter = APIRouter()
logging.basicConfig(level=logging.INFO)


@authorityRouter.get("/authority/inbox/", response_model=list[AuthroityInboxModel] )
def read_emails(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    emails =  db.query(AuthroityInbox).order_by(desc(AuthroityInbox.date)).offset(skip).limit(limit).all()
    serialized_emails = [serialize_email_authority(email) for email in emails]
    # return emails
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"emails":serialized_emails}
    )


@authorityRouter.get("/authority/inbox/{sender_email}", response_model=list[AuthroityInboxModel] )
def read_specific_email(sender_email: str , skip: int = 0, limit: int = 10 ,db: Session = Depends(get_db)):
    emails = db.query(AuthroityInbox).order_by(desc(AuthroityInbox.date)).filter(AuthroityInbox.from_ == sender_email).all()
    serialized_emails = [serialize_email_authority(email) for email in emails]
    if not emails:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No emails found for sender {sender_email}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"emails":serialized_emails}
    )

@authorityRouter.delete("/authority/inbox/")
async def delete_emails(db: Session = Depends(get_db)):
    db.query(AuthroityInbox).delete()
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"msg": "Successfully Deleted Emails"}
    )
