import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _as_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///expense_tracker.db'
    )
    if SQLALCHEMY_DATABASE_URI.startswith('mysql://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('mysql://', 'mysql+pymysql://', 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Use SQLite-safe engine options when connecting to SQLite.
    # check_same_thread=False is safe here because SQLAlchemy's connection
    # pool ensures each thread gets its own connection.
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {'check_same_thread': False},
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
            'pool_recycle': 280,
        }

    DEBUG = _as_bool('FLASK_DEBUG', False)
    AUTO_CREATE_TABLES = _as_bool('AUTO_CREATE_TABLES', False)

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

    # Market Data Settings
    MARKET_UPDATE_INTERVAL = 30  # seconds
