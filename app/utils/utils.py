from app.data.schemas.customer_inbox import CustomerInbox
import re
from app.data.schemas.customer import Customer
from app.data.schemas.replies import EmailReply


def serialize_email(email: CustomerInbox) -> dict:
    return {
        "name":email.name,
        "id": email.id,
        "subject": email.subject,
        "from_": email.from_,
        "to": email.to,
        "date": email.date.isoformat() if email.date else None,
        "message_id": email.message_id,
        "body": email.body,
        "content_type": email.content_type,
        "email_type":email.email_type,
        "metadata": email.get_metadata(),
        "contact_id":email.contact_id
    }


def serialize_reply(email: EmailReply) -> dict:
    return {
        "name":email.name,
        "id": email.id,
        "subject": email.subject,
        "from_": email.from_,
        "to": email.to,
        "date": email.date.isoformat() if email.date else None,
        "message_id": email.message_id,
        "body": email.body,
        "content_type": email.content_type,
        "email_type":email.email_type,
        "metadata": email.get_metadata(),
        "parent_message_id":email.parent_message_id
    }


def serialize_email_authority(email: CustomerInbox) -> dict:
    return {
        "name":email.name,
        "id": email.id,
        "subject": email.subject,
        "from_": email.from_,
        "to": email.to,
        "date": email.date.isoformat() if email.date else None,
        "message_id": email.message_id,
        "body": email.body,
        "content_type": email.content_type,
        "email_type":email.email_type,
        "metadata": email.get_metadata(),
    }

def serialize_Contact(contact: Customer) -> dict:
    return {
        "name":contact.name,
        "id": contact.id,
        "email": contact.email,
        "date": contact.date.isoformat() if contact.date else None,
        "application_number":contact.application_number,
        "email_count":contact.email_count
    }
def extract_name(text):
    name_regex = r'^(.*?) <.*>$'
    match = re.match(name_regex, text)
    return match.group(1).strip() if match else None
