from app.data.schemas.email import Email
import re
from app.data.schemas.contact import Contact


def serialize_email(email: Email) -> dict:
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
        "metadata": email.get_metadata()
    }

def serialize_Contact(contact: Contact) -> dict:
    return {
        "name":contact.name,
        "id": contact.id,
        "email": contact.email,
        "date": contact.date.isoformat() if contact.date else None,
        "message_id": contact.message_id,
    }
def extract_name(text):
    name_regex = r'^(.*?) <.*>$'
    match = re.match(name_regex, text)
    return match.group(1).strip() if match else None
