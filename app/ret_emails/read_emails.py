import imaplib
import email
from email.header import decode_header
from ..data.models.email import EmailModel
from datetime import datetime


def fetch_latest_email(imap_server: str, username: str, password: str, mailbox: str = "inbox",num_emails: int = 10):
    try:
        count = 0
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select(mailbox)
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print("No messages found!")
            return []

        email_ids = messages[0].split()
        if not email_ids:
            print("No email IDs found!")
            return []
        latest_email_ids = email_ids[-num_emails:]

        emails = []

        for email_id in latest_email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")

            if status != "OK":
                print(f"Failed to fetch email with ID {email_id}!")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
 
                    body = None
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" not in content_disposition:
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                                elif content_type == "text/html":
                                    html_body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    else:
                        body = msg.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    if not body and html_body:
                        body = html_body

                    from_ = str(msg.get("From"))
                    message_ids = msg.get("Message-ID")
                    contentType =  msg.get("Content-Type")
                    date =  str(msg.get("Date"))
                    date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
                    to = str(msg.get("To"))
                    metaData = dict(msg)
                    tempEmail = EmailModel(from_ = from_ ,to=  to , metadata= metaData , content_type= contentType , date=date , message_id = message_ids , subject=subject , body=body ) 
                    emails.append(tempEmail)

        return emails

    finally:
        mail.close()
        mail.logout()