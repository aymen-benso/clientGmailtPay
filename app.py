import imaplib
import email
from email.header import decode_header

# IMAP settings
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL = 'aymenbensoltana2@@gmail.com'
PASSWORD = 'a1y2m3e4n5'

def decode_subject(encoded_subject):
    decoded_parts = decode_header(encoded_subject)
    subject = 'linda'
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            subject += part.decode(charset or 'utf-8')
        else:
            subject += part
    return subject

def get_emails():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    # Login to your account
    mail.login(EMAIL, PASSWORD)
    # Select the mailbox (inbox)
    mail.select('inbox')

    # Search for emails
    result, data = mail.search(None, 'ALL')
    if result == 'OK':
        # Get the list of email IDs
        email_ids = data[0].split()
        # Loop through each email ID
        for email_id in email_ids:
            # Fetch the email
            result, data = mail.fetch(email_id, '(RFC822)')
            if result == 'OK':
                # Parse the email
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                # Decode and print the subject
                subject = decode_subject(msg['Subject'])
                print('Subject:', subject)
                # Decode and print the body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            print('Body:', body)
                else:
                    body = msg.get_payload(decode=True).decode()
                    print('Body:', body)
                print('---')

    # Logout from the server
    mail.logout()

if __name__ == '__main__':
    get_emails()
