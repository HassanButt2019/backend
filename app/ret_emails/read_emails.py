import imaplib
import email
from email.header import decode_header
import re

from bs4 import BeautifulSoup

from app.data.models.email_reply import EmailReplyModel
from ..data.models.customer_inbox import CustomerInboxModel
from datetime import datetime
from ..utils.utils import extract_name


import email
import imaplib
from email.header import decode_header
from datetime import datetime
import re

def fetch_latest_email(imap_server: str, username: str, password: str, mailbox: str = "inbox", batch_size: int = 50):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select(mailbox)

        # Search for all email IDs in the inbox
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print("No messages found!")
            return []

        email_ids = messages[0].split()
        if not email_ids:
            print("No email IDs found!")
            return []

        print("Total emails:", len(email_ids))

        # Fetch emails in batches
        emails = []
        for start in range(0, len(email_ids), batch_size):
            end = min(start + batch_size, len(email_ids))
            batch_ids = email_ids[start:end]
            batch_ids_str = ",".join(batch_ids)

            # Fetch the batch of emails
            status, msg_data = mail.fetch(batch_ids_str, "(RFC822)")
            if status != "OK":
                print(f"Failed to fetch emails in batch {start}-{end}!")
                continue

            # Process each message in the batch
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0] if msg["Subject"] else ("No Subject", None)

                    # Decode the subject if necessary
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or 'utf-8')

                    body, html_body = None, None

                    # Handle email parts (multipart emails)
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" not in content_disposition:
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                                elif content_type == "text/html":
                                    html_body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                    else:
                        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='replace')

                    if not body and html_body:
                        body = html_body

                    name = extract_name(str(msg.get("From")))
                    from_ = str(msg.get("From"))
                    message_ids = msg.get("Message-ID")
                    contentType = msg.get("Content-Type")
                    date = str(msg.get("Date"))
                    date_str_cleaned = re.sub(r"\s*\(.*\)", "", date)
                    date = datetime.strptime(date_str_cleaned, "%a, %d %b %Y %H:%M:%S %z")
                    to = str(msg.get("To"))
                    metaData = dict(msg)

                    tempEmail = CustomerInboxModel(
                        name=name, from_=from_, to=to, metadata=metaData,
                        content_type=contentType, date=date, message_id=message_ids,
                        subject=subject, body=body, email_type=mailbox
                    )
                    emails.append(tempEmail)

            print(f"Fetched {len(emails)} emails so far.")

        return emails

    finally:
        try:
            mail.close()
        except imaplib.IMAP4.error:
            print("Could not close the mailbox. It might not have been selected.")
        mail.logout()





def fetch_sent_emails(imap_server: str, username: str, password: str, num_emails: int = 4000):
    """
    Fetches the latest emails from the Sent mailbox and extracts the body content.

    :param imap_server: The IMAP server address.
    :param username: The email account username.
    :param password: The email account password.
    :param num_emails: The number of recent emails to fetch.
    :return: A list of email objects from the Sent mailbox.
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select("Sent")  # Assuming "Gesendet" is the Sent mailbox

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
                if msg["Subject"]:
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or 'utf-8')
                else:
                    subject = "No Subject" 

                    body = None
                    html_body = None

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" not in content_disposition:
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                                elif content_type == "text/html":
                                    html_body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                                    # Use BeautifulSoup to extract plain text from HTML
                                    soup = BeautifulSoup(html_body, "html.parser")
                                    body = soup.get_text()
                    else:
                        # Handle single-part messages
                        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')

                    soup = BeautifulSoup(body, "html.parser")
                    body = soup.get_text()
                    if not body and html_body:
                        body = html_body

                    name = "Migrando"
                    from_ = str(msg.get("From"))
                    message_ids = msg.get("Message-ID")
                    contentType = msg.get("Content-Type")
                    date = str(msg.get("Date"))

                    try:
                        date = convert_date_format(date_str=date)
                    except ValueError as e:
                        print(f"Date parsing error: {e}")
                        continue  # Skip this email if date parsing fails

                    to = str(msg.get("To"))
                    metaData = dict(msg)
                    
                    tempEmail = CustomerInboxModel(name=name, from_=from_, to=to, metadata=metaData,
                                                   content_type=contentType, date=date, message_id=message_ids,
                                                   subject=subject, body=body, email_type="Gesendet")
                    emails.append(tempEmail)

        return emails

    finally:
        try:
            mail.close()
        except imaplib.IMAP4.error:
            print("Could not close the mailbox. It might not have been selected.")
        mail.logout()


def fetch_replies(imap_server: str, username: str, password: str, original_message_id: str, mailbox: str = "inbox"):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select(mailbox)
        search_criteria = f'(HEADER "In-Reply-To" "{original_message_id}")'
        status, messages = mail.search(None, search_criteria)
        if status != "OK":
            print("No replies found!")
            return []

        email_ids = messages[0].split()
        if not email_ids:
            print("No email IDs found!")
            return []
        emails = []
        for email_id in email_ids:
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
                    name = extract_name(str(msg.get("From")))
                    from_ = str(msg.get("From"))
                    message_ids = msg.get("Message-ID")
                    content_type = msg.get("Content-Type")
                    date = str(msg.get("Date"))
                    date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
                    to = str(msg.get("To"))
                    meta_data = dict(msg)
                    temp_email = EmailReplyModel(name=name, from_=from_, to=to, metadata=meta_data, content_type=content_type, date=date, message_id=message_ids, subject=subject, body=body, email_type=mailbox , parent_message_id= original_message_id)
                    emails.append(temp_email)
        
        return emails

    finally:
        try:
            mail.close()
        except imaplib.IMAP4.error:
            print("Could not close the mailbox. It might not have been selected.")
        mail.logout()  # Always log out after completing












def convert_date_format(date_str: str) -> str:
    """
    Converts a date string from the format "Mon, 16 Sep 2024 13:53:18 +0200 (CET)" to "2024-09-16 13:53:18.000000".

    :param date_str: The date string to be converted.
    :return: The formatted date string.
    """
    try:
        # Parse the original date string
        parsed_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z (CET)")
        
        # Convert to the desired format
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S.%f")
        return formatted_date
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return None