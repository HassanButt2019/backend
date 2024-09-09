import logging
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc

from app.data.models.contact import ContactModel
from ...database.db import   get_db
from app.data.schemas.contact import Contact
from sqlalchemy.orm import Session
import os
from ...utils.utils import serialize_Contact, serialize_email

contactRouter = APIRouter()
logging.basicConfig(level=logging.INFO)



@contactRouter.get("/contacts/", response_model=list[ContactModel] )
def read_contacts(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    contacts =  db.query(Contact).order_by(desc(Contact.date)).offset(skip).limit(limit).all()
    serialized_contacts = [serialize_Contact(contact) for contact in contacts]
    # return contacts
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"contacts":serialized_contacts}
    )


@contactRouter.get("/contacts/{sender_email}", response_model=list[ContactModel] )
def read_specific_contact(sender_email: str , skip: int = 0, limit: int = 10 ,db: Session = Depends(get_db)):
    contacts = db.query(Contact).order_by(desc(Contact.date)).filter(Contact.from_ == sender_email).all()
    serialized_contacts = [serialize_Contact(contact) for contact in contacts]
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No contacts found for sender {sender_email}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"contacts":serialized_contacts}
    )

@contactRouter.delete("/contacts/")
async def delete_contacts(db: Session = Depends(get_db)):
    db.query(Contact).delete()
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"msg": "Successfully Deleted contacts"}
    )
