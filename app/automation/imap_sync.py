
import time
import threading
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.ret_emails.read_emails import fetch_latest_email, fetch_sent_emails
from ..database.db import  get_db , SessionLocal
import os
from dotenv import load_dotenv
from ..database.crud import create_email




load_dotenv() 

def email_sync_worker(imap_server: str, username: str, password: str,db: Session = Depends(get_db)):
    while True:
        all_mail_box = []
        inbox_emails = fetch_latest_email(imap_server, username, password , mailbox="INBOX")
        sent_emails = fetch_sent_emails(imap_server,username,password)
        all_mail_box.append(inbox_emails)
        # all_mail_box.append(sent_emails)
        for mail_box in all_mail_box:
            for email in mail_box:
                create_email(
                email=email,
                db=db
            )
            
        time.sleep(1) 


def start_email_sync():
    imap_server = os.getenv("IMAP_SERVER")
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    db = SessionLocal()
    threading.Thread(target=email_sync_worker, args=(imap_server, username, password, db)).start()