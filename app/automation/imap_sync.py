
import time
import threading
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.ret_emails.read_emails import fetch_latest_email
from ..database.db import  get_db , SessionLocal
import os
from dotenv import load_dotenv
from ..database.crud import create_email




load_dotenv() 

def email_sync_worker(imap_server: str, username: str, password: str,db: Session = Depends(get_db)):
    while True:
        emails = fetch_latest_email(imap_server, username, password)
        print(len(emails))
        for email in emails:
            create_email(
                subject=email["subject"],
                body=email["body"],
                from_=email["from"],
                message_id=email["message_id"],
                db=db
            )
        time.sleep(1) 


def start_email_sync():

    imap_server = os.getenv("IMAP_SERVER")
    username = "testmail@migrando.de"
    password = "KxBHfJksz8T5wU5dULxN"
    db = SessionLocal()
    threading.Thread(target=email_sync_worker, args=(imap_server, username, password, db)).start()