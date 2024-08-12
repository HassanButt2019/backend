from fastapi import FastAPI, Depends, HTTPException
from app.ret_emails.read_emails import fetch_latest_email
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.crud import init_db
from typing import List

from app.data.schemas.email import Email

load_dotenv()
app = FastAPI()
# Initialize the database
init_db()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI email reader!"}

@app.get("/store-email" )
def  read_emails():

    latest_email = fetch_latest_email(imap_server, username, password)
    db = SessionLocal()
    try:
        yield db
        if latest_email:
            for email in latest_email:
                db_email = Email(subject=email["subject"] ,body=email["body"] ,from_=email["from"])
                db.add(db_email)
                db.commit()
                db.refresh(db_email)
            return {"emails": "List of emails will be here."}
        else:
            print("No email found or an error occurred.")
        return {"emails": "List of emails will be here."}
    finally:
        db.close()
                    




@app.get("/emails/")
def read_emails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Email).offset(skip).limit(limit).all()


def create_email(subject: str, from_: str, body: str, db: Session = Depends(get_db)):
    print(subject)
