"""
Send emails via Gmail SMTP.
Requires a Gmail App Password (not your normal password):
https://myaccount.google.com/apppasswords
Set ASSISTANT_EMAIL and ASSISTANT_EMAIL_PASSWORD as environment variables.
"""
import smtplib
from email.mime.text import MIMEText

import config


def send_email(to_address: str, subject: str, body: str) -> str:
    if not config.EMAIL_ADDRESS or not config.EMAIL_APP_PASSWORD:
        return "Email isn't set up yet — add ASSISTANT_EMAIL and ASSISTANT_EMAIL_PASSWORD."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = to_address

    try:
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(config.EMAIL_ADDRESS, config.EMAIL_APP_PASSWORD)
            server.sendmail(config.EMAIL_ADDRESS, [to_address], msg.as_string())
        return f"Email sent to {to_address}."
    except smtplib.SMTPAuthenticationError:
        return "Email login failed — check your app password."
    except Exception as e:
        return f"Couldn't send the email: {e}"
