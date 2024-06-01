import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
from decouple import config

SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT')
SMTP_USERNAME = config('SMTP_USERNAME')
SMTP_PASSWORD = config('SMTP_PASSWORD')

class SendMail:

    @staticmethod
    def send_raw(sub:str,body:str,to:str):
        message = MIMEMultipart()
        message["From"] = SMTP_USERNAME
        message["To"] = to
        message["Subject"] = sub
        message.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        try:

            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD) 

            server.sendmail(SMTP_USERNAME, to, message.as_string())
            print("Email sent successfully")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            server.quit()
