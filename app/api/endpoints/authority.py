import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import asc, desc

from app.data.models.authority import AuthroityModel
from ...database.db import  to_json, get_db
from ...ret_emails.read_emails import fetch_latest_email
from app.data.schemas.authority import Authroity
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ...database.crud import create_email
import os
from ...utils.utils import serialize_email

authorityRouter = APIRouter()
logging.basicConfig(level=logging.INFO)


@authorityRouter.get("/authority/inbox/", response_model=list[AuthroityModel] )
def read_emails(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    emails =  db.query(Authroity).order_by(desc(Authroity.date)).offset(skip).limit(limit).all()
    serialized_emails = [serialize_email(email) for email in emails]
    # return emails
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"emails":serialized_emails}
    )


@authorityRouter.get("/authority/inbox/{sender_email}", response_model=list[AuthroityModel] )
def read_specific_email(sender_email: str , skip: int = 0, limit: int = 10 ,db: Session = Depends(get_db)):
    emails = db.query(Authroity).order_by(desc(Authroity.date)).filter(Authroity.from_ == sender_email).all()
    serialized_emails = [serialize_email(email) for email in emails]
    if not emails:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No emails found for sender {sender_email}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"emails":serialized_emails}
    )

@authorityRouter.delete("/authority/inbox/")
async def delete_emails(db: Session = Depends(get_db)):
    db.query(Authroity).delete()
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"msg": "Successfully Deleted Emails"}
    )
