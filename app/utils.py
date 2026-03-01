import random
import string
import requests
from datetime import datetime, timedelta
from config import Config

GAS_EMAIL_URL = (
    'https://script.google.com/macros/s/'
    'AKfycbxoStF25frOY88NGrFemsiDqIoTgOD3sQzUYF6kwp4rTXHlmH3AlZRR9caNMTwDzIrl/exec'
)


def send_otp_email(email, otp, username):
    """Send OTP verification email via Google Apps Script Web App API.

    Returns True when the OTP has been delivered successfully.
    """
    payload = {"recipient": email, "otp": otp, "username": username}
    try:
        resp = requests.post(GAS_EMAIL_URL, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"[OTP][GAS] Response for {email}: {resp.text}")
        return True
    except Exception as e:
        print(f"[OTP][GAS] Error sending OTP to {email}: {e}")
        return False


def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=Config.OTP_LENGTH))


def get_otp_expiry_time():
    """Get OTP expiry time"""
    return datetime.utcnow() + timedelta(minutes=Config.OTP_EXPIRY_MINUTES)
