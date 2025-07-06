import os
import re
import smtplib
from email.message import EmailMessage


def valid_email(email: str) -> bool:
    """Helper function to validate email address

    Args:
        email: email address

    Returns:
        indicator if email is valid
    """
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return True
    return False


def send_email(
    email_body: str,
    subject: str = "Email from kayjan.fly.dev Web App",
    recipient: str = "kayjanw@gmail.com",
) -> bool:
    """Helper function to send email

    Args:
        email_body: email body to be sent
        subject: email subject to be sent
        recipient: email recipient to receive email

    Returns:
        indicator if email is sent
    """
    try:
        GOOGLE_APP_PW = ENV["GOOGLE_APP_PW"]
    except NameError:
        try:
            GOOGLE_APP_PW = os.environ["GOOGLE_APP_PW"]
        except KeyError:
            print("No GOOGLE_APP_PW found")
    try:
        msg = EmailMessage()
        from_email = "kayjanw@gmail.com"  # verified sender
        msg.set_content(email_body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, GOOGLE_APP_PW)
            smtp.send_message(msg)
        return True
    except Exception:
        return False
