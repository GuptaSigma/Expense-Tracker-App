import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, storage_uri=os.getenv('RATELIMIT_STORAGE_URI', 'memory://'))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure SQLite file uses an absolute, writable path in deploy environments.
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if isinstance(db_uri, str) and db_uri.startswith('sqlite:///'):
        sqlite_path = db_uri.replace('sqlite:///', '', 1)
        if sqlite_path and sqlite_path != ':memory:':
            is_absolute = os.path.isabs(sqlite_path) or (len(sqlite_path) > 1 and sqlite_path[1] == ':')
            if not is_absolute:
                sqlite_path = os.path.join(app.instance_path, sqlite_path)
                app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{sqlite_path}"
            sqlite_dir = os.path.dirname(sqlite_path)
            if sqlite_dir:
                os.makedirs(sqlite_dir, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from app.routes import main
    from app.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Auto-create schema for SQLite (so a fresh deploy works without migrations)
    # or when AUTO_CREATE_TABLES is explicitly enabled for other databases.
    if db_uri.startswith('sqlite') or app.config.get('AUTO_CREATE_TABLES', False):
        with app.app_context():
            db.create_all()

    return app


# Backward-compatible WSGI entrypoint so `gunicorn app:app` also works.
app = create_app()
