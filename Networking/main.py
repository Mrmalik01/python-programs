import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import dotenv
import os
import ssl

dotenv.load_dotenv()

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
TO = "khizarmalik.ai@gmail.com"


# Name of the server through which the email will be sent
context = ssl.create_default_context()
server  = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)

# To start the whole process
server.ehlo()

server.login(EMAIL, PASSWORD)

# Email contains various parts
msg  = MIMEMultipart()

msg['From'] = "Chic-Chic"
msg['To'] = TO
msg['Subject'] = "Chic-Chic Launched"

with open("message.txt", "r") as f:
    message = f.read()
    f.close()

# Adding the body to the email
msg.attach(MIMEText(message, "plain"))

attachment_path = "message.txt"

# Read the file as binary
attachment = open(attachment_path, "rb")

# To convert the file into some format
payload = MIMEBase("application", "ocetet-stream")
payload.set_payload(attachment.read())

encoders.encode_base64(payload)
payload.add_header("Content-Disposition", f'attachment; filename={attachment_path}')
msg.attach(payload)

text = msg.as_string()

server.sendmail(EMAIL, TO, text)
