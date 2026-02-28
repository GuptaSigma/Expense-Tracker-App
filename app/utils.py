import random
import string
from datetime import datetime, timedelta
from flask import render_template_string
from flask_mail import Mail, Message
from config import Config

mail = Mail()


def send_otp_email(email, otp, username):
    """Send OTP verification email.

    Returns True when the OTP has been delivered (or simulated) successfully.
    Behaviour is controlled by three env vars:
      DISABLE_EMAIL_OTP – skip SMTP and return False; auth.py then decides
                          whether to auto-verify (no OTP_DEV_MODE) or show the
                          dev OTP banner (OTP_DEV_MODE=true).
      OTP_DEV_MODE      – log the OTP to the console instead of sending email.
      MAIL_TIMEOUT      – seconds to wait for the SMTP connection (default 10).
    """
    if Config.DISABLE_EMAIL_OTP:
        print(f"[DISABLE_EMAIL_OTP] Skipping OTP email for {email}")
        return False

    if Config.OTP_DEV_MODE:
        print(f"[OTP_DEV_MODE] OTP for {email} ({username}): {otp}")
        return True

    if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
        print(f"Email not configured. OTP for {email}: {otp}")
        return False

    try:
        subject = "ExpenseTracker - OTP Verification"
        html_body = f"""
        <html>
            <body style="font-family: 'Plus Jakarta Sans', Arial; background-color: #f8fafc; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #0f172a; margin: 0;">ExpenseTracker</h1>
                        <p style="color: #64748b; margin: 5px 0 0 0;">Verify Your Email</p>
                    </div>
                    
                    <div style="margin-bottom: 30px;">
                        <p style="color: #334155; font-size: 16px; margin-bottom: 20px;">Hi <strong>{username}</strong>,</p>
                        <p style="color: #334155; font-size: 16px; margin-bottom: 20px;">Thank you for signing up! To complete your registration, please verify your email using the OTP below:</p>
                        
                        <div style="background: #f1f5f9; border: 2px solid #e2e8f0; border-radius: 8px; padding: 20px; text-align: center; margin: 30px 0;">
                            <p style="color: #1e293b; font-size: 32px; font-weight: bold; margin: 0; letter-spacing: 8px;">{otp}</p>
                        </div>
                        
                        <p style="color: #94a3b8; font-size: 14px; margin-top: 20px;">This OTP will expire in 10 minutes.</p>
                    </div>
                    
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center;">
                        <p style="color: #94a3b8; font-size: 12px; margin: 0;">If you didn't sign up for this account, please ignore this email.</p>
                        <p style="color: #94a3b8; font-size: 12px; margin: 10px 0 0 0;">© 2026 ExpenseTracker. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        msg = Message(
            subject=subject,
            recipients=[email],
            html=html_body,
            sender=Config.MAIL_DEFAULT_SENDER
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")
        return False


def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=Config.OTP_LENGTH))


def get_otp_expiry_time():
    """Get OTP expiry time"""
    return datetime.utcnow() + timedelta(minutes=Config.OTP_EXPIRY_MINUTES)
