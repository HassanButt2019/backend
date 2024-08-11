import imaplib
import email
from email.header import decode_header

username = "testmail@migrando.de"
password = "KxBHfJksz8T5wU5dULxN"
mail = imaplib.IMAP4_SSL("w01ae1f1.kasserver.com")
mail.login(username, password)
mail.select("inbox")

# Search for all emails in the inbox
status, messages = mail.search(None, "ALL")

# Convert messages to a list of email IDs
print(messages)
email_ids = messages[0].split()
for email_id in email_ids[-1:]:  # Fetch the latest email; use email_ids if you want all emails
    status, msg_data = mail.fetch(email_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Parse the email content
            msg = email.message_from_bytes(response_part[1])
            # Decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # If it's a bytes type, decode to str
                subject = subject.decode(encoding if encoding else "utf-8")
            # Decode the email sender
            from_ = msg.get("From")
            print("Subject:", subject)
            print("From:", from_)

            # If the email message is multipart
            if msg.is_multipart():
                # Iterate over email parts
                for part in msg.walk():
                    # Extract content type of the email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    # Get the email body
                    if "attachment" not in content_disposition:
                        # Decode the email body if needed
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            body = part.get_payload()
                        print("Body:", body)
            else:
                # If the email message isn't multipart
                content_type = msg.get_content_type()
                body = msg.get_payload(decode=True).decode()
                print("Body:", body)

# Close the connection and logout
mail.close()
mail.logout()
