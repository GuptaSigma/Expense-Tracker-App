import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config import Config


def send_otp_email(email, otp, username):
    """Send OTP verification email via Gmail SMTP.

    Returns True when the OTP has been delivered successfully.
    """
    mail_username = Config.MAIL_USERNAME
    mail_password = Config.MAIL_PASSWORD

    if not mail_username or not mail_password:
        print(
            "[OTP] MAIL_USERNAME or MAIL_PASSWORD is missing or blank. "
            "Set the environment variables for Gmail SMTP. "
            f"OTP for {email}: {otp}"
        )
        return False

    print(f"[OTP] Sending OTP email to {email} via SMTP | Sender: {mail_username}")

    subject = "ExpenseTracker OTP Verification"
    body = (
        f"Hi {username},\n\n"
        f"Thank you for signing up! To complete your registration, "
        f"please verify your email using the OTP below:\n\n"
        f"Your OTP code is: {otp}\n\n"
        f"This OTP will expire in 10 minutes.\n\n"
        f"If you didn't sign up for this account, please ignore this email.\n\n"
        f"© 2026 ExpenseTracker. All rights reserved."
    )

    msg = MIMEMultipart()
    msg["From"] = mail_username
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        try:
            if Config.MAIL_USE_TLS:
                server.starttls()
            server.login(mail_username, mail_password)
            server.sendmail(mail_username, email, msg.as_string())
        finally:
            server.quit()
        print(f"[OTP] Email delivered successfully to {email}")
        return True
    except Exception as e:
        print(f"[OTP] Failed to send OTP via SMTP: {e}")
        return False


def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=Config.OTP_LENGTH))


def get_otp_expiry_time():
    """Get OTP expiry time"""
    return datetime.utcnow() + timedelta(minutes=Config.OTP_EXPIRY_MINUTES)
