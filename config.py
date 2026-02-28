import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _as_int(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default


def _as_bool(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')

    _db_url = os.getenv('DATABASE_URL')
    if not _db_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Set it to a PostgreSQL connection string, e.g. "
            "postgresql://user:password@host/dbname"
        )
    # Normalize driver prefixes so SQLAlchemy picks the right dialect.
    if _db_url.startswith('postgresql://'):
        _db_url = _db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    elif _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    elif _db_url.startswith('mysql://'):
        _db_url = _db_url.replace('mysql://', 'mysql+pymysql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }

    DEBUG = _as_bool('FLASK_DEBUG', False)
    AUTO_CREATE_TABLES = _as_bool('AUTO_CREATE_TABLES', False)
    RUN_MIGRATIONS = _as_bool('RUN_MIGRATIONS', False)

    # Cookie and CSRF security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = _as_bool('SESSION_COOKIE_SECURE', not DEBUG)
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    REMEMBER_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE
    WTF_CSRF_TIME_LIMIT = None

    # Rate limit defaults
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '200 per day;50 per hour')

    # OpenRouter API Configuration - For AI Suggestions & Investment Advice
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
    OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'openai/gpt-4o-mini')

    # GoldAPI Configuration
    GOLD_API_KEY = os.getenv('GOLD_API_KEY')
    GOLD_API_URL = 'https://www.goldapi.io/api'

    # Gemini API Configuration - For Chatbox
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = 'http://localhost:5000/auth/google/callback'

    # Resend API Configuration (for OTP email delivery)
    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
    RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
    RESEND_TIMEOUT = _as_int('RESEND_TIMEOUT', 15)

    # OTP Settings
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10

    # Market Data Settings
    MARKET_UPDATE_INTERVAL = 30  # seconds
