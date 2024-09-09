from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from app.database.crud import init_db
from typing import List
import logging
from fastapi.middleware.cors import CORSMiddleware
from .automation.imap_sync import start_email_sync
from .api.endpoints.email import emailRouter
from .api.endpoints.authority import authorityRouter
from .api.endpoints.contact import contactRouter

CONFIG_FORMATTER = '%(asctime)s %(name)s[%(levelname)s] %(message)s'
logger = logging.getLogger(__name__)

def setup_logging():
    """Set log level to INFO for debugging."""
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level)
    logging.basicConfig(level=log_level, format=CONFIG_FORMATTER)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to specific origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup_event():
    init_db()
    start_email_sync()




@app.get("/")
def read_root():
    return {"msg": "This is Email Project"}



app.include_router(emailRouter)
app.include_router(authorityRouter)
app.include_router(contactRouter)

setup_logging()




