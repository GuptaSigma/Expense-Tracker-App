from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app import db, limiter, mail
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from config import Config
from app.utils import generate_otp, send_otp_email, get_otp_expiry_time
from datetime import datetime

oauth = OAuth()

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit('10 per minute')
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'warning')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
@limiter.limit('5 per minute')
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'warning')
            return render_template('register.html')

        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash('Username already exists', 'warning')
        elif email_exists:
            flash('Email already registered', 'warning')
        else:
            # Generate OTP
            otp = generate_otp()
            
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                otp=otp,
                otp_expiry=get_otp_expiry_time()
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Send OTP email
            if send_otp_email(email, otp, username):
                session['pending_verification_email'] = email
                flash('Registration successful! OTP sent to your email.', 'success')
                return redirect(url_for('auth.verify_otp'))
            else:
                # If email fails, still allow login but warn
                flash('Registration successful but OTP email failed. Contact support.', 'warning')
                return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/verify-otp', methods=['GET', 'POST'])
@limiter.limit('10 per minute')
def verify_otp():
    """Verify OTP for email verification"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        otp = request.form.get('otp', '').strip()
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('User not found', 'warning')
            return render_template('verify_otp.html')
        
        if not user.otp or not user.otp_expiry:
            flash('No OTP found. Please register again.', 'warning')
            return redirect(url_for('auth.register'))
        
        # Check if OTP expired
        if datetime.utcnow() > user.otp_expiry:
            flash('OTP has expired. Please request a new one.', 'warning')
            return render_template('verify_otp.html')
        
        # Verify OTP
        if user.otp == otp:
            user.is_email_verified = True
            user.otp = None
            user.otp_expiry = None
            db.session.commit()
            
            flash('Email verified successfully! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid OTP. Please try again.', 'warning')
    
    return render_template('verify_otp.html')


@auth.route('/resend-otp', methods=['POST'])
@limiter.limit('3 per minute')
def resend_otp():
    """Resend OTP to email"""
    email = request.form.get('email', '').strip().lower()
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash('User not found', 'warning')
        return redirect(url_for('auth.verify_otp'))
    
    # Generate new OTP
    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = get_otp_expiry_time()
    db.session.commit()
    
    # Send new OTP
    if send_otp_email(email, otp, user.username):
        flash('OTP sent to your email!', 'success')
    else:
        flash('Failed to send OTP. Please try again.', 'danger')
    
    return redirect(url_for('auth.verify_otp'))


# Google OAuth Routes
def init_google_oauth(app):
    """Initialize Google OAuth with Flask app"""
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )


@auth.route('/auth/google')
def google_login():
    """Redirect user to Google for login"""
    if not Config.GOOGLE_CLIENT_ID or not Config.GOOGLE_CLIENT_SECRET:
        flash('Google authentication is not configured', 'warning')
        return redirect(url_for('auth.login'))
    
    google = oauth.google
    redirect_uri = url_for('auth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth.route('/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    if not Config.GOOGLE_CLIENT_ID or not Config.GOOGLE_CLIENT_SECRET:
        flash('Google authentication is not configured', 'warning')
        return redirect(url_for('auth.login'))
    
    google = oauth.google
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash('Failed to get user information from Google', 'warning')
            return redirect(url_for('auth.login'))
        
        google_id = user_info.get('sub')
        email = user_info.get('email')
        name = user_info.get('name', email.split('@')[0])
        
        # Check if user with this google_id already exists
        user = User.query.filter_by(google_id=google_id).first()
        
        if not user:
            # Check if email already exists
            user = User.query.filter_by(email=email).first()
            
            if user:
                # Link Google account to existing user
                user.google_id = google_id
            else:
                # Create new user
                user = User(
                    username=name,
                    email=email,
                    google_id=google_id,
                    password=generate_password_hash('google-oauth')  # Placeholder password
                )
            
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        flash(f'Welcome {user.username}!', 'success')
        return redirect(url_for('main.dashboard'))
    
    except Exception as e:
        flash(f'Error during Google authentication: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))
