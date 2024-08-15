from app.data.schemas.email import Email


def serialize_email(email: Email) -> dict:
    return {
        "id": email.id,
        "subject": email.subject,
        "from_": email.from_,
        "to": email.to,
        "date": email.date.isoformat() if email.date else None,
        "message_id": email.message_id,
        "body": email.body,
        "content_type": email.content_type,
        "metadata": email.get_metadata()
    }
