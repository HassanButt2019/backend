from email.quoprimime import unquote
import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc

from app.data.models.authority_inbox import AuthroityInboxModel
from app.data.models.email_reply import EmailReplyModel
from app.data.schemas.replies import EmailReply
from ...database.db import  to_json, get_db
from ...ret_emails.read_emails import fetch_replies
from app.data.schemas.authority_inbox import AuthroityInbox
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ...database.crud import create_email, create_reply
import os
from ...utils.utils import serialize_email, serialize_email_authority, serialize_reply

replyRouter = APIRouter()
logging.basicConfig(level=logging.INFO)


# @replyRouter.get("/read-replies", response_model=list[EmailReplyModel] )
# def read_replies_by_email(skip: int = 0, limit: int = 30 , parent_message_id: str = Query(..., description="The id of the message"), db: Session = Depends(get_db)):
#     decoded_message_id = unquote(parent_message_id)
#     print(decoded_message_id)
#     imap_server = os.getenv("IMAP_SERVER")
#     username = "testmail2@migrando.de"
#     password = os.getenv("EMAIL_PASSWORD")
#     all_mailbox_emails = []
#     inbox_email = fetch_replies(imap_server, username, password ,decoded_message_id,mailbox="inbox")
#     all_mailbox_emails.append(inbox_email)
#     try:
#         if inbox_email:
#             for reply in inbox_email:
#                     create_reply(reply , db=db)
#             return JSONResponse(
#                         status_code=status.HTTP_201_CREATED,
#                         content={
#                             "msg":f"Successfully stored replies , storedLength {len(all_mailbox_emails)}"}
#                     )

                
#         else:
#             print("No email found or an error occurred.")
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"msg": "Unable To Store Emails"}
#         )
#     finally:
#         db.close()



@replyRouter.get("/replies/", response_model=list[EmailReplyModel] )
def read_emails(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    emails =  db.query(EmailReply).order_by(desc(EmailReply.date)).offset(skip).limit(limit).all()
    serialized_emails = [serialize_reply(email) for email in emails]
    # return emails
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"replies":serialized_emails}
    )